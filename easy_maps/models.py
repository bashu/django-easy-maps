# -*- coding: utf-8 -*-

import logging
import sys

try:
    from collections.abc import Callable
except ImportError:
    from collections import Callable

from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import geocode
from .conf import settings
from .utils import importpath

logger = logging.getLogger(__name__)


class AddressManager(models.Manager):
    def for_address(self, address):
        obj, created = self.get_or_create(address=address)

        if timezone.now() > obj.expiry() and not created:
            obj.save()  # trigger fetching once again

        return obj


class Address(models.Model):

    address = models.CharField(_("address"), max_length=255, unique=True)

    # for internal use...

    computed_address = models.CharField(_("computed address"), max_length=255, null=True, blank=True)
    latitude = models.FloatField(_("latitude"), null=True, blank=True)
    longitude = models.FloatField(_("longitude"), null=True, blank=True)

    exception = models.TextField(_("has exception?"), blank=True)

    timestamp = models.DateTimeField(auto_now=True)

    objects = AddressManager()

    class Meta:
        verbose_name = _("EasyMaps Address")
        verbose_name_plural = _("Address Geocoding Cache")

    def __str__(self):
        return self.address

    def expiry(self, *args, **kwargs):
        return self.timestamp + timedelta(seconds=settings.EASY_MAPS_CACHE_LIFETIME)

    def fetch(self):
        if not self.address:
            return None

        func = getattr(settings, "EASY_MAPS_GEOCODE", None)
        if func is not None:
            if not isinstance(func, Callable):
                func = importpath(func)

        try:
            self.computed_address, (
                self.latitude,
                self.longitude,
            ) = func(self.address)
        except geocode.Error as e:
            self.computed_address = self.latitude = self.longitude = None  # shit happens

            try:
                logger.error(e)
            except Exception:
                logger.error("Geocoding error for address '%s'", address)

            self.exception = "{0.__name__}: {1}".format(sys.exc_info()[0], sys.exc_info()[1])

    def has_exception(self):
        return bool(self.exception)

    has_exception.short_description = _("has exception?")
    has_exception.boolean = True

    def save(self, *args, **kwargs):
        if bool(self.computed_address) is False:  # just in case
            self.longitude = self.latitude = None

        if (self.longitude is None) or (self.latitude is None):
            self.fetch()

        super(Address, self).save(*args, **kwargs)
