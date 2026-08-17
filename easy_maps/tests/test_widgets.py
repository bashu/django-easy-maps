from django import forms
from django.test import TestCase
from django.test.utils import override_settings

from easy_maps.models import Address
from easy_maps.widgets import AddressWithMapWidget


class AddressWithMapWidgetTest(TestCase):
    fake_default_center = (1, 2)

    def setUp(self):
        self.field = forms.CharField(required=False, widget=AddressWithMapWidget)

    def test_render_includes_the_plain_text_input(self):
        response = self.field.widget.render("address", "cached", {"id": "id_address"})
        assert "<input" in response
        assert 'name="address"' in response
        assert 'value="cached"' in response

    @override_settings(EASY_MAPS_CENTER=fake_default_center)
    def test_render_without_value_falls_back_to_default_center(self):
        # a falsy value means parse_address() falls back to EASY_MAPS_CENTER
        # instead of hitting the geocoder, so this stays a DB/network-free test
        response = self.field.widget.render("address", None, {"id": "id_address"})
        assert "map-canvas-" in response
        assert "gm-err-container" in response

    def test_render_with_cached_address_shows_the_map(self):
        # pre-create the Address with its geocoded fields already set, so
        # for_address() hits the cache instead of calling the real geocoder
        Address.objects.create(
            address="cached",
            computed_address="Cached, Somewhere",
            latitude=1,
            longitude=2,
        )

        response = self.field.widget.render("address", "cached", {"id": "id_address"})

        assert "google.maps.Map(" in response
        assert "gm-err-container" not in response
