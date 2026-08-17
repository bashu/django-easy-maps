from unittest import mock

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings

import pytest

from easy_maps.conf import settings
from easy_maps.models import Address


class EasyMapTest(TestCase):
    fake_default_center = (1, 2)

    def test_empty_dont_save_on_db(self):
        # If we pass an empty address we don't save nothing in the
        # database
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        n_addresses_before = len(Address.objects.all())

        t = template.Template(html % {"v": ""})
        t.render(template.Context({}))

        n_addresses_after = len(Address.objects.all())

        assert n_addresses_after == n_addresses_before

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_empty_address_use_defaults(self):
        # When an empty address is passed uses the EASY_MAPS_CENTER
        # setting
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        address = [None]  # nonlocal

        # below we patch the render_to_string in order to retrieve the
        # map context variable and check its coordinate
        def get_address_instance(*args, **kwargs):
            _template_name, context = args
            address[0] = context["map"]
            return ""

        t = template.Template(html % {"v": ""})
        with mock.patch("classytags.helpers.render_to_string", get_address_instance):
            t.render(template.Context({}))

        assert address[0].latitude == EasyMapTest.fake_default_center[0]
        assert address[0].longitude == EasyMapTest.fake_default_center[1]

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_normal_address(self):
        # If we pass an address don't use the defaults
        html = "{%% load easy_maps_tags %%}{%% easy_map '%(v)s' 500 500 10 %%}"

        n_addresses_before = len(Address.objects.all())

        a = "Ekaterinburg, Mira 33"

        t = template.Template(html % {"v": a})
        t.render(template.Context({}))

        address = Address.objects.get(address=a)

        assert address.latitude != EasyMapTest.fake_default_center[0]
        assert address.longitude != EasyMapTest.fake_default_center[1]

        n_addresses_after = len(Address.objects.all())

        assert n_addresses_after == n_addresses_before + 1

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
        assert n_addresses_after == n_addresses_before

    def test_address_instance_without_zoom_uses_default_zoom(self):
        # Passing an Address instance skips the Address.objects.for_address()
        # branch in parse_address() entirely (no queries), and omitting zoom
        # exercises the EASY_MAPS_ZOOM fallback in get_context().
        html = "{% load easy_maps_tags %}{% easy_map address 500 500 %}"

        a = Address.objects.create(
            address="fake",
            computed_address="Fake, Somewhere",
            latitude=1,
            longitude=2,
        )

        t = template.Template(html)
        with self.assertNumQueries(0):
            rendered = t.render(template.Context({"address": a}))

        assert f"zoom: {settings.EASY_MAPS_ZOOM}" in rendered

    def test_wrong_number_of_args_raises_template_syntax_error(self):
        # address + width with no height is exactly the "len(params) == 2"
        # case the tag explicitly rejects
        html = "{% load easy_maps_tags %}{% easy_map 'Ekaterinburg, Mira 33' 500 %}"

        t = template.Template(html)
        with pytest.raises(template.TemplateSyntaxError):
            t.render(template.Context({}))

    @override_settings(EASY_MAPS_GOOGLE_KEY=None)
    def test_missing_google_key_raises_improperly_configured(self):
        # The argument-count check passes here (4 params), so this
        # exercises the EASY_MAPS_GOOGLE_KEY guard specifically -- it's
        # raised before parse_address() is ever called, so no geocoding
        # happens either.
        html = (
            "{% load easy_maps_tags %}{% easy_map 'Ekaterinburg, Mira 33' 500 500 10 %}"
        )

        t = template.Template(html)
        with pytest.raises(ImproperlyConfigured):
            t.render(template.Context({}))
