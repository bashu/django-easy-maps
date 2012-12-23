from django.contrib import admin
from django import forms
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .models import Address
from .widgets import AddressWithMapWidget
from .geo import geolocalize

import simplejson


class AddressAdmin(admin.ModelAdmin):
    list_display = ['address', 'computed_address', 'latitude', 'longitude', 'geocode_error']
    list_filter = ['geocode_error']
    search_fields = ['address']

    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }

    def get_urls(self):
        """Add a view that serves geolocalized data on POST request
        """
        urls = super(AddressAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^geo/$', self.admin_site.admin_view(self.get_geo), name='address_json'),
        )
        return my_urls + urls

    # FIXME: add CSRF protection look at https://docs.djangoproject.com/en/1.4/ref/contrib/csrf/#ajax
    # for example in passing a CSRF token
    @csrf_exempt
    def get_geo(self, request):
        """Return a json that will be used to insert correct value
        into the model form.
        """
        if request.method != "POST" or not request.POST.has_key('address') or request.POST['address'] == '':
            return HttpResponseBadRequest()

        computed_address, latitude, longitude, geocode_error = geolocalize(request.POST["address"])
        return HttpResponse(simplejson.dumps(
            {
                'computed_address': computed_address,
                'latitude':         latitude,
                'longitude':        longitude,
                'geocode_error':    geocode_error,
            }
        ), content_type='application/json')

class AddressAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'address': AddressWithMapWidget({'class': 'vTextField'})
        }

class AddressInlineAdmin(admin.StackedInline):
    extra = 1
    form = AddressAdminForm
