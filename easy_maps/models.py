from __future__ import absolute_import
import logging

from django.conf import settings
from django.db import models

from . import geocode

logger = logging.getLogger(__name__)


class Address(models.Model):
    address = models.CharField(max_length=255, unique=True)
    computed_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geocode_error = models.BooleanField(default=False)

    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return
        try:
            do_geocode = getattr(settings, "EASY_MAPS_GEOCODE", geocode.google_v3)
            self.computed_address, (self.latitude, self.longitude,) = do_geocode(self.address)
            self.geocode_error = False
        except geocode.Error as e:
            try:
                logger.error(e)
            except Exception:
                logger.error("Geocoding error for address %s", self.address)

            self.geocode_error = True
            # TODO: store the exception

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name = "EasyMaps Address"
        verbose_name_plural = "Address Geocoding Cache"

