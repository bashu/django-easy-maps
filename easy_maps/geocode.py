# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str

from geopy import geocoders
from geopy.exc import GeocoderServiceError

from .conf import settings


class Error(Exception):
    pass


def google_v3(address):
    """
    Given an address, return ``(computed_address, (latitude, longitude))``
    tuple using Google Geocoding API v3.

    """
    try:
        g = geocoders.GoogleV3(api_key=settings.EASY_MAPS_GOOGLE_KEY)

        results = g.geocode(smart_str(address), exactly_one=False)
        if results is not None:
            return results[0]

        raise Error("No results found for '%s'" % address)
    except (UnboundLocalError, ValueError, GeocoderServiceError) as e:
        raise Error(e)
