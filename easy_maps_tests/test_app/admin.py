# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.contrib import admin
from easy_maps.admin import AddressAdmin
from easy_maps.models import Address

admin.site.register(Address, AddressAdmin)
