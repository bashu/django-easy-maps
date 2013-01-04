from django.conf import settings
from django.utils.encoding import smart_str

from geopy import geocoders

def geolocalize(address):
    """From an address return the values needed to fullify an Address model form
    """
    try:
        if hasattr(settings, "EASY_MAPS_GOOGLE_KEY") and settings.EASY_MAPS_GOOGLE_KEY:
            g = geocoders.Google(settings.EASY_MAPS_GOOGLE_KEY)
        else:
            g = geocoders.Google(resource='maps')
        s_address = smart_str(address)
        computed_address, (latitude, longitude,) = g.geocode(s_address, exactly_one=False)[0]
        geocode_error = False
    except (UnboundLocalError, ValueError,geocoders.google.GQueryError):
        geocode_error = True

    return computed_address, latitude, longitude, geocode_error
