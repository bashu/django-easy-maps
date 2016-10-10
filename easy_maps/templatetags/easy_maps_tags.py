# -*- coding: utf-8 -*-

from django import template

from classytags.core import Options
from classytags.helpers import InclusionTag
from classytags.arguments import Argument, IntegerArgument

from ..conf import settings
from ..models import Address

register = template.Library()


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
        IntegerArgument('zoom', required=False, default=None),
        'using',
        Argument('template_name', default=None, required=False),
    )

    def render_tag(self, context, **kwargs):
        params = dict((k, v) for k, v in kwargs.items() if v and k not in ['template_name'])
        if 'address' in params and (len(params) == 2 or len(params) > 4):
            raise template.TemplateSyntaxError(
                "easy_map tag has the following syntax: "
                "{% easy_map <address> [<width> <height>] [zoom] [using <template_name>] %}"
            )
        return super(EasyMapTag, self).render_tag(context, **kwargs)

    def get_template(self, context, **kwargs):
        return kwargs.get('template_name', None) or self.template

    def parse_address(self, address=None):
        if isinstance(address, Address):
            return address

        if not address:
            return Address(
                latitude=settings.EASY_MAPS_CENTER[0],
                longitude=settings.EASY_MAPS_CENTER[1],
            )
        else:
            return Address.objects.get_or_create(address=address)[0]

        raise NotImplementedError

    def get_context(self, context, **kwargs):
        kwargs.update({'map': self.parse_address(kwargs.pop('address'))})
        if not kwargs.get('zoom', None):
            kwargs['zoom'] = 16  # default value
        return kwargs

register.tag(EasyMapTag)
