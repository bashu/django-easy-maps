from django.db import models

from .geo import geolocalize
from . import settings


class Address(models.Model):
    address = models.CharField(max_length=255, db_index=True)
    computed_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(default=settings.EASY_MAPS_CENTER_LAT, null=True, blank=True)
    longitude = models.FloatField(default=settings.EASY_MAPS_CENTER_LON, null=True, blank=True)
    geocode_error = models.BooleanField(default=False)

    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return

        self.computed_address, self.latitude, self.longitude, self.geocode_error = geolocalize(self.address)

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

