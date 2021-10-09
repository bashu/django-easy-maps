# -*- coding: utf-8 -*-

import mock

from django import template
from django.test import TestCase
from django.test.utils import override_settings

from easy_maps.models import Address


class AddressTests(TestCase):
    fake_default_center = (1, 2)

    def test_empty_dont_save_on_db(self):
        # If we pass an empty address we don't save nothing in the
        # database
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        n_addresses_before = len(Address.objects.all())

        t = template.Template(html % {"v": ""})
        t.render(template.Context({}))

        n_addresses_after = len(Address.objects.all())

        self.assertEqual(n_addresses_after, n_addresses_before)

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_empty_address_use_defaults(self):
        # When an empty address is passed uses the EASY_MAPS_CENTER
        # setting
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        address = [None]  # nonlocal

        # below we patch the render_to_string in order to retrieve the
        # map context variable and check its coordinate
        def get_address_instance(*args, **kwargs):
            template_name, context = args
            address[0] = context["map"]
            return ""

        t = template.Template(html % {"v": ""})
        with mock.patch("classytags.helpers.render_to_string", get_address_instance):
            t.render(template.Context({}))

        self.assertEqual(address[0].latitude, AddressTests.fake_default_center[0])
        self.assertEqual(address[0].longitude, AddressTests.fake_default_center[1])

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_normal_address(self):
        # If we pass an address don't use the defaults
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        n_addresses_before = len(Address.objects.all())

        a = "Ekaterinburg, Mira 33"

        t = template.Template(html % {"v": a})
        t.render(template.Context({}))

        address = Address.objects.get(address=a)

        self.assertNotEqual(address.latitude, AddressTests.fake_default_center[0])
        self.assertNotEqual(address.longitude, AddressTests.fake_default_center[1])

        n_addresses_after = len(Address.objects.all())

        self.assertEqual(n_addresses_after, n_addresses_before + 1)

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_use_address_instance(self):
        # It's possible to pass directly to the easy_map tag an
        # Address instance.  This test checks also that the database
        # is not hit.
        html = "{%% load easy_maps_tags %%}{%% easy_map %(v)s 500 500 10 %%}"

        # create a fake address
        a = Address.objects.create(address="fake")

        n_addresses_before = len(Address.objects.all())

        t = template.Template(html % {"v": "address"})
        ctx = template.Context({"v": a})

        self.assertNumQueries(0, lambda: t.render(ctx))

        n_addresses_after = len(Address.objects.all())

        # no address is created in the process
        self.assertEqual(n_addresses_after, n_addresses_before)
