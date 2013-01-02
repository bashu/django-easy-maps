#coding: utf-8
from django import template
from django.template.loader import render_to_string
from easy_maps.models import Address
from .. import settings

register = template.Library()

@register.tag
def easy_map(parser, token):
    """
    The syntax:

        {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

    or

        {% easy_map <addresses> [<width> <height>] [<zoom>] [using <template_name>] %}

    where in the second case you pass a queryset containing the addresses to be
    visualized.
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
        try:
            address = self.address.resolve(context) or ''
            template_name = self.template_name.resolve(context)

            if isinstance(address, basestring):
                # if not exists the searched address then created an unsaved instance
                try:
                    address = Address.objects.get(address=address)
                except:
                    address = Address(address=address)

                address = [address,]

            context.update({
                'markers': address,
                'width': self.width,
                'height': self.height,
                # FIXME: if the list is empty?
                'latitude': address[0].latitude,
                'longitude': address[0].longitude,
                'zoom': self.zoom,
                'template_name': template_name
            })
            return render_to_string(template_name, context_instance=context)
        except template.VariableDoesNotExist:
            return ''
