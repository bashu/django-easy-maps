from django.test import TestCase
from django.template import Template, Context
import mock
from django.test.utils import override_settings

from .models import Address


class AddressTests(TestCase):
    fake_default_center  = (1, 2)
    def test_empty_dont_save_on_db(self):
        """If we pass an empty address we don't save nothing in the database"""
        n_addresses_before = len(Address.objects.all())

        simple_template_string = """{% load easy_maps_tags %}
        {% easy_map "" 500 500 10 %}
        """
        t = Template(simple_template_string)
        t.render(Context({}))


        n_addresses_after = len(Address.objects.all())

        self.assertEqual(n_addresses_after, n_addresses_before)

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_empty_address_use_defaults(self):
        """When an empty address is passed uses the EASY_MAPS_CENTER setting"""
        a = ""
        simple_template_string = """{%% load easy_maps_tags %%}
        {%% easy_map "%s" 500 500 10 %%}
        """ % a
        self.address = None
        # below we patch the render_to_string in order to retrieve the map
        # context variable and check its coordinate
        def get_map_context_instance(*args, **kwargs):
            self.address = (kwargs['context_instance'].dicts[1])['map']
            return ''

        t = Template(simple_template_string)
        with mock.patch('easy_maps.templatetags.easy_maps_tags.render_to_string', get_map_context_instance):
            t.render(Context({}))

        self.assertEqual(self.address.latitude, AddressTests.fake_default_center[0])
        self.assertEqual(self.address.longitude, AddressTests.fake_default_center[1])

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_normal_address(self):
        """If we pass an address don't use the defaults"""
        n_addresses_before = len(Address.objects.all())

        a = "Ekaterinburg, Mira 33"
        simple_template_string = """{%% load easy_maps_tags %%}
        {%% easy_map "%s" 500 500 10 %%}
        """ % a
        t = Template(simple_template_string)
        t.render(Context({}))

        address = Address.objects.get(address=a)
        self.assertNotEqual(address.latitude, AddressTests.fake_default_center[0])
        self.assertNotEqual(address.longitude, AddressTests.fake_default_center[1])

        n_addresses_after = len(Address.objects.all())

        self.assertEqual(n_addresses_after, n_addresses_before + 1)

