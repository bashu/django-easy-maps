from django.contrib import admin
from django import forms

from .widgets import AddressWithMapWidget

class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'computed_address', 'latitude', 'longitude', 'geocode_error']
    list_filter = ['geocode_error']
    search_fields = ['address']

    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }
