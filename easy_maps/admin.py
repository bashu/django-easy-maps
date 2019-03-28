# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin

from .models import Address
from .widgets import AddressWithMapWidget


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'address', 'computed_address', 'latitude', 'longitude']
    list_filter = ['geocode_error']
    search_fields = ['address']

    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }
