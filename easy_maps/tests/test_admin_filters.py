from django.contrib import admin
from django.test import RequestFactory
from django.test import TestCase

from easy_maps.admin import AddressAdmin
from easy_maps.admin import HasExceptionFilter
from easy_maps.models import Address


class HasExceptionFilterTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = AddressAdmin(Address, admin.site)

        # created with computed_address/lat/lng already set so Address.save()
        # doesn't trigger a real geocode() call
        self.clean = Address.objects.create(
            address="clean",
            computed_address="clean",
            latitude=1,
            longitude=2,
        )
        self.broken = Address.objects.create(
            address="broken",
            computed_address="broken",
            latitude=1,
            longitude=2,
        )
        self.broken.exception = "GeocoderServiceError: boom"
        self.broken.save(update_fields=["exception"])

    def test_lookups(self):
        request = self.factory.get("/")
        f = HasExceptionFilter(request, {}, Address, self.model_admin)
        assert f.lookups(request, self.model_admin) == ((1, "Yes"), (0, "No"))

    def test_queryset_no_value_is_noop(self):
        request = self.factory.get("/")
        f = HasExceptionFilter(request, {}, Address, self.model_admin)
        assert set(f.queryset(request, Address.objects.all())) == {
            self.clean,
            self.broken,
        }

    def test_queryset_has_exception_only(self):
        params = {"has_exception": "1"}
        request = self.factory.get("/", params)
        f = HasExceptionFilter(request, params, Address, self.model_admin)
        qs = f.queryset(request, Address.objects.all())
        assert list(qs) == [self.broken]
        assert self.clean not in qs

    def test_queryset_no_exception_only(self):
        params = {"has_exception": "0"}
        request = self.factory.get("/", params)
        f = HasExceptionFilter(request, params, Address, self.model_admin)
        qs = f.queryset(request, Address.objects.all())
        assert list(qs) == [self.clean]
        assert self.broken not in qs
