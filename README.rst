================
django-easy-maps
================

This app makes it easy to display a map for given address in django templates.
The license is MIT.

Installation
============

::

    pip install geopy
    pip install django-easy-maps

Usage
=====

1. Add 'easy_maps' to INSTALLED_APPS

2. Run ``./manage.py syncdb`` (or ``./manage.py migrate easy_maps``
   if south is in use)

3. Use the ``easy_map`` templatetag::

       {% load easy_maps_tags %}

       <!-- Default map with 300x400 dimensions -->
       {% easy_map "Russia, Ekaterinburg, Mira 32" 300 400 %}

       <!-- Variable address, custom detail level and custom template -->
       {% easy_map address 200 200 5 using 'map.html' %}

   It has the following signature::

       {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

   The coordinates for map will be obtained using google geocoder on first
   access. Then they'll be cached in DB. Django's template caching can be used
   later in order to prevent DB access on each map render::

       {% load easy_maps_tags cache %}

       {% cache 600 my_map firm.address %}
           {% easy_map firm.address 300 400 %}
       {% endcache %}

That's all! No API keys, manual geocoding, html/js copy-pasting or
django model changes is needed.

Customization
=============

If the default map template is not sufficient then custom map template can be
used::

   {% easy_map address using 'map.html' %}

   <!-- or -->

   {% easy_map address 200 300 5 using 'map.html' %}

The template will have 'map' (it is the ``easy_maps.models.Address`` instance),
'width', 'height' and 'zoom' variables. The outer template context is passed
to 'map.html' as well.

Address model
=============

easy_maps.models.Address model has the following fields:

* address
* computed address
* longtitude
* latitude
* geocode_error

Contributing
============

If you've found a bug, implemented a feature or customized the template and
think it is useful then please consider contributing. Patches, pull requests or
just suggestions are welcome!

Source code: https://bitbucket.org/kmike/django-easy-maps/

Bug tracker: https://bitbucket.org/kmike/django-easy-maps/issues/new

