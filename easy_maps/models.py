from django.db import models
from geopy import geocoders

class Address(models.Model):
    address = models.CharField(max_length=255, db_index=True)
    computed_address = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longtitude = models.FloatField(null=True, blank=True)
    geocode_error = models.BooleanField(default=False)

    def fill_geocode_data(self):
        try:
            g = geocoders.Google(resource='maps')
            address = self.address.encode('utf8')
            self.computed_address, (self.latitude, self.longtitude,) = g.geocode(address)
            self.geocode_error = False
        except (UnboundLocalError, ValueError,):
            self.geocode_error = True

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if (self.longtitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(Address, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address
