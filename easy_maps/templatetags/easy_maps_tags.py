# -*- coding: utf-8 -*-

from django import template
from django.core.exceptions import ImproperlyConfigured

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument, IntegerArgument

from ..conf import settings
from ..models import Address

register = template.Library()

CENTER = settings.EASY_MAPS_CENTER
GOOGLE_MAPS_API_KEY = settings.EASY_MAPS_GOOGLE_MAPS_API_KEY


def parse_address(address=None):
    if isinstance(address, Address):
        return address

    if not address:
        return Address(latitude=CENTER[0], longitude=CENTER[1])

    return Address.objects.get_or_create(address=address)[0]


class EasyMapTag(InclusionTag):
    """
    The syntax:

    {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

    The "address" parameter can be an ``easy_maps.Address`` instance
    or a string describing it.  If an address is not found a new entry
    is created in the database.

    """
    name = 'easy_map'
    template = 'easy_maps/map.html'
    options = Options(
        Argument('address', resolve=True, required=True),
        IntegerArgument('width', required=False, default=None),
        IntegerArgument('height', required=False, default=None),
        IntegerArgument('zoom', required=False, default=16),
        'using',
        Argument('template_name', default=None, required=False),
    )

    def get_template(self, context, **kwargs):
        return kwargs.get('template_name', None) or self.template

    def get_context(self, context, **kwargs):
        params = dict((k, v) for k, v in kwargs.items() if v is not None)
        if len(params.keys()) == 3 or len(params.keys()) > 5:
            raise template.TemplateSyntaxError(
                "easy_map tag has the following syntax: "
                "{% easy_map <address> [<width> <height>] [zoom] [using <template_name>] %}"
            )

        if GOOGLE_MAPS_API_KEY is None:
            raise ImproperlyConfigured(
                "easy_map tag requires EASY_MAPS_GOOGLE_MAPS_API_KEY to be set in global settings "
                "because of the restrictions introduced in Google Maps API v3 by Google, Inc."
            )

        context['width'] = kwargs.get('width')
        context['height'] = kwargs.get('height')
        context['zoom'] = kwargs.get('zoom')
        context['map'] = parse_address(kwargs.pop('address'))
        context['key'] = GOOGLE_MAPS_API_KEY

        return context

register.tag(EasyMapTag)
