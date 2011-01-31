from django.conf import settings
from django.db import models
from django.utils.encoding import smart_str
from geopy import geocoders

class Address(models.Model):
    address = models.CharField(max_length=255, db_index=True)
    computed_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    geocode_error = models.BooleanField(default=False)

    def fill_geocode_data(self):
        if not self.address:
            self.geocode_error = True
            return
        try:
            if hasattr(settings, "EASY_MAPS_GOOGLE_KEY") and settings.EASY_MAPS_GOOGLE_KEY:
                g = geocoders.Google(settings.EASY_MAPS_GOOGLE_KEY)
            else:
                g = geocoders.Google(resource='maps')
            address = smart_str(self.address)
            self.computed_address, (self.latitude, self.longitude,) = g.geocode(address)
            self.geocode_error = False
        except (UnboundLocalError, ValueError,geocoders.google.GQueryError):
            self.geocode_error = True

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address
