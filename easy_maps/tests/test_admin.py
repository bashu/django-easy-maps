from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.test import TestCase

from easy_maps.admin import AddressAdmin
from easy_maps.admin import HasExceptionFilter
from easy_maps.models import Address
from easy_maps.widgets import AddressWithMapWidget


class AddressAdminTest(TestCase):
    def setUp(self):
        self.model_admin = AddressAdmin(Address, admin.site)

        self.superuser = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",  # noqa: S106
        )
        request = RequestFactory().get("/admin/easy_maps/address/add/")
        request.user = self.superuser
        self.form_class = self.model_admin.get_form(request)

    def test_list_display(self):
        assert self.model_admin.list_display == [
            "address",
            "computed_address",
            "latitude",
            "longitude",
            "has_exception",
        ]

    def test_list_filter_uses_has_exception_filter(self):
        assert self.model_admin.list_filter == [HasExceptionFilter]

    def test_search_fields(self):
        assert self.model_admin.search_fields == ["address"]

    def test_address_field_uses_map_widget(self):
        form = self.form_class()

        assert isinstance(form.fields["address"].widget, AddressWithMapWidget)
