from django.forms import TextInput
from django.template import Template, Context

class AddressWithMapWidget(TextInput):
    class Media:
        js = (
            'https://maps.google.com/maps/api/js?sensor=false',
            'js/easy_maps.js',
        )
    def render(self, name, value, attrs=None):
        # retrieve the field's id otherwise it's not possible
        # to use correctly the JS
        _id = attrs["id"]

        # we assume two conditions on 'id'
        assert _id.find('id_') == 0

        find_id = _id.find('address')
        assert find_id > 0

        _id = _id[:find_id]
        default_html = super(AddressWithMapWidget, self).render(name, value, attrs)
        map_template = Template("""<button type='button' onclick='easy_maps_bind_button("{{ id }}")'>update</button>{% load easy_maps_tags %}{% easy_map address 700 200 16 %}""")

        context = Context({'id': _id, 'id_safe': _id.replace('-', '_'), 'address': value})
        return default_html + map_template.render(context)
