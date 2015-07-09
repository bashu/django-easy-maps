# -*- coding: utf-8 -*-

import mock

from django import template
from django.test import TestCase

try:
    from django.test.utils import override_settings
except ImportError:
    from django.utils import unittest

    def override_settings(*args, **kwargs):
        return unittest.skip("overriding settings is not supported by this django version")

from .models import Address


class AddressTests(TestCase):
    fake_default_center = (1, 2)

    def test_empty_dont_save_on_db(self):
        # If we pass an empty address we don't save nothing in the
        # database
        html = """{%% load easy_maps_tags %%}{%% easy_map '%(varname)s' 500 500 10 %%}"""
    
        before_count = len(Address.objects.all())

        t = template.Template(html % {"varname": ""})
        t.render(template.Context({}))

        after_count = len(Address.objects.all())

        self.assertEqual(after_count, before_count)

    # @override_settings(EASY_MAPS_CENTER=fake_default_center)
    # def test_empty_address_use_defaults(self):
    #     """When an empty address is passed uses the EASY_MAPS_CENTER setting"""
    #     a = ""
    #     simple_template_string = """{%% load easy_maps_tags %%}
    #     {%% easy_map "%s" 500 500 10 %%}
    #     """ % a

    #     address = [None]  # nonlocal

    #     # below we patch the render_to_string in order to retrieve the map
    #     # context variable and check its coordinate
    #     def get_map_context_instance(*args, **kwargs):
    #         address[0] = kwargs['context_instance']['map']
    #         return ''

    #     t = template.Template(simple_template_string)
    #     with mock.patch('easy_maps.templatetags.easy_maps_tags.render_to_string', get_map_context_instance):
    #         t.render(template.Context({}))

    #     self.assertEqual(address[0].latitude, AddressTests.fake_default_center[0])
    #     self.assertEqual(address[0].longitude, AddressTests.fake_default_center[1])

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_normal_address(self):
        # If we pass an address don't use the defaults
        html = """{%% load easy_maps_tags %%}{%% easy_map '%(varname)s' 500 500 10 %%}"""

        before = len(Address.objects.all())

        a = "Ekaterinburg, Mira 33"
        
        t = template.Template(html % {"varname": a})
        t.render(template.Context({}))

        address = Address.objects.get(address=a)

        self.assertNotEqual(address.latitude, AddressTests.fake_default_center[0])
        self.assertNotEqual(address.longitude, AddressTests.fake_default_center[1])

        after = len(Address.objects.all())

        self.assertEqual(after, before + 1)

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_use_address_instance(self):
        # It's possible to pass directly to the easy_map tag an Address instance.
        # This test checks also that the database is not hit.
        html = """{%% load easy_maps_tags %%}{%% easy_map %(varname)s 500 500 10 %%}"""

        # create a fake address
        a = Address.objects.create(address='fake')

        before = len(Address.objects.all())

        t = template.Template(html % {'varname': 'address'})
        ctx = template.Context({'varname': a})

        self.assertNumQueries(0, lambda: t.render(ctx))

        after = len(Address.objects.all())

        # no new records are created in the process
        self.assertEqual(after, before)
