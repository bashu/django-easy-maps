# -*- coding: utf-8 -*-

import logging
import collections

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import geocode
from .conf import settings
from .utils import importpath

logger = logging.getLogger(__name__)


class AddressManager(models.Manager):

    def for_address(self, address):
        if not address:
            return None

        func = getattr(settings, 'EASY_MAPS_GEOCODE', None)
        if func is not None:
            if not isinstance(func, collections.Callable):
                func = importpath(func)

        try:
            return func(address)
        except geocode.Error as e:
            try:
                logger.error(e)
            except Exception:
                logger.error("Geocoding error for address '%s'", address)

        return None


@python_2_unicode_compatible  
class Address(models.Model):

    address = models.CharField(_('address'), max_length=255, unique=True)

    # for internal use...
    
    computed_address = models.CharField(_('computed address'), max_length=255, null=True, blank=True)
    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)

    # TODO: replace this crap with something better
    geocode_error = models.BooleanField(_('geocode error'), default=False)

    objects = AddressManager()
    
    class Meta:
        verbose_name = _("EasyMaps Address")
        verbose_name_plural = _("Address Geocoding Cache")

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if (self.longitude is None) or (self.latitude is None):
            loc = self.__class__.objects.for_address(self.address)
            if loc is not None:
                self.computed_address, (self.latitude, self.longitude,) = loc
            else:  # TODO: replace this crap with something better
                self.computed_address = None
        super(Address, self).save(*args, **kwargs)

