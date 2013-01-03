from django.conf import settings

EASY_MAPS_CENTER_LAT = getattr(settings, 'EASY_MAPS_CENTER_LAT', -34.397)
EASY_MAPS_CENTER_LON = getattr(settings, 'EASY_MAPS_CENTER_LON', 150.644)
