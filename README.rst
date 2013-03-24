================
django-easy-maps
================

This app makes it easy to display a map for given address in django templates.
No API keys, manual geocoding, html/js copy-pasting or django model
changes is needed.

The license is MIT.

Installation
============

::

    pip install 'geopy >= 0.95'
    pip install django-easy-maps

Then add 'easy_maps' to INSTALLED_APPS and run ``./manage.py syncdb``
(or ``./manage.py migrate easy_maps`` if South is in use)

Settings
========

If you need a place where center the map when no address is inserted yet add
the latitude and longitude to the EASY_MAPS_CENTER variable in your
settings.py like the following::

    EASY_MAPS_CENTER = (-41.3, 32)

Sometimes you can run into Google Maps API lockdown. If this happens
then create a EASY_MAPS_GOOGLE_KEY in your settings.py file::

    EASY_MAPS_GOOGLE_KEY = "your-google-maps-api-key"

Usage
=====

This app provides an ``easy_map`` template tag::

    {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

Examples::

    {% load easy_maps_tags %}

    <!-- Default map with 300x400 dimensions -->
    {% easy_map "Russia, Ekaterinburg, Mira 32" 300 400 %}

    <!-- Variable address, custom detail level and custom template -->
    {% easy_map address 200 200 5 using 'map.html' %}

The coordinates for map will be obtained using google geocoder on first
access. Then they'll be cached in DB. Django's template caching can be used
later in order to prevent DB access on each map render::

    {% load easy_maps_tags cache %}

    {% cache 600 my_map firm.address %}
        {% easy_map firm.address 300 400 %}
    {% endcache %}

Customization
=============

If the default map template is not sufficient then custom map template can be
used. Examples::

   {% easy_map address using 'map.html' %}
   {% easy_map address 200 300 5 using 'map.html' %}

The template will have 'map' (it is the ``easy_maps.models.Address``
instance auto-created for passed address on first access), 'width',
'height' and 'zoom' variables. The outer template context is passed
to rendered template as well.

The default template can be found here:
https://bitbucket.org/kmike/django-easy-maps/src/tip/easy_maps/templates/easy_maps/map.html

You can start your own template from scratch or just override some blocks in the
default template.

Please refer to http://code.google.com/apis/maps/documentation/javascript/ for
detailed Google Maps JavaScript API help.

Customizing geocoder
--------------------

To use a custom geocoder set EASY_MAPS_GEOCODE option::

    # settings.py

    from django_easy_maps import geocode

    def my_geocode(address):
        """
        Given an address (an unicode string), return
        ``(computed_address, (latitude, longitude))`` tuple.
        """
        try:
            # ...
            return computed_address, (latitude, longitude)
        except (...) as e:
            raise geocode.Error(e)

    EASY_MAPS_GEOCODE = my_geocode



Address model
=============

``easy_maps.models.Address`` model has the following fields:

* address - the requested address
* computed_address - address returned by geocoder
* longitude
* latitude
* geocode_error - True if geocoder wasn't able to handle the address

Address model should be considered implementation detail. Its purpose is
to avoid using geocoder for each request, that's a kind of persistent cache.
It is included in readme because information about available data can
be useful for custom map templates.

Admin address preview
=====================

django-easy-maps provides basic widget that displays a map under the address
field. It can be used in admin for map previews. Example usage::

    from django import forms
    from django.contrib import admin
    from easy_maps.widgets import AddressWithMapWidget
    from firms.models import Firm

    class FirmAdmin(admin.ModelAdmin):
        class form(forms.ModelForm):
            class Meta:
                widgets = {
                    'address': AddressWithMapWidget({'class': 'vTextField'})
                }

    admin.site.register(Firm, FirmAdmin)

'address' field should be a CharField or TextField.

Contributing
============

If you've found a bug, implemented a feature or customized the template and
think it is useful then please consider contributing. Patches, pull requests or
just suggestions are welcome!

Source code: https://bitbucket.org/kmike/django-easy-maps/

Bug tracker: https://bitbucket.org/kmike/django-easy-maps/issues/new
