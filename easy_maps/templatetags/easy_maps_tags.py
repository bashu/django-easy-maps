#coding: utf-8
from django import template
from django.template.loader import render_to_string
from easy_maps.models import Address
from django.conf import settings

register = template.Library()

@register.tag
def easy_map(parser, token):
    """
    The syntax:
        {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

    The "address" parameter can be an Address instance or a string describing it.
    If an address is not found a new entry is created in the database.
    """
    width, height, zoom, template_name = None, None, None, None
    params = token.split_contents()

    # pop the template name
    if params[-2] == 'using':
        template_name = params[-1]
        params = params[:-2]

    if len(params) < 2:
        raise template.TemplateSyntaxError('easy_map tag requires address argument')

    address = params[1]

    if len(params) == 4:
        width, height = params[2], params[3]
    elif len(params) == 5:
        width, height, zoom = params[2], params[3], params[4]
    elif len(params) == 3 or len(params) > 5:
        raise template.TemplateSyntaxError('easy_map tag has the following syntax: '
                   '{% easy_map <address> <width> <height> [zoom] [using <template_name>] %}')
    return EasyMapNode(address, width, height, zoom, template_name)

class EasyMapNode(template.Node):
    def __init__(self, address, width, height, zoom, template_name):
        self.address = template.Variable(address)
        self.width = width or ''
        self.height = height or ''
        self.zoom = zoom or 16
        self.template_name = template.Variable(template_name or '"easy_maps/map.html"')

    def render(self, context):
        address = self.address.resolve(context)
        template_name = self.template_name.resolve(context)

        map = address
        if not isinstance(address, Address):
            if address == '':
                map = Address(latitude=settings.EASY_MAPS_CENTER[0], longitude=settings.EASY_MAPS_CENTER[1])
            else:
                map, _ = Address.objects.get_or_create(address=address)

        context.update({
            'map': map,
            'width': self.width,
            'height': self.height,
            'zoom': self.zoom,
            'template_name': template_name
        })
        return render_to_string(template_name, context_instance=context)
