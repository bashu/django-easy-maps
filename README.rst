django-easy-maps
================

This app makes it easy to display a map for given address in django templates.
No API keys, manual geocoding, html/js copy-pasting or django model
changes is needed.

Authored by `Mikhail Korobov <http://kmike.ru/>`_, and some great
`contributors <https://github.com/kmike/django-easy-maps/contributors>`_.

.. image:: https://img.shields.io/pypi/v/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/pypi/dm/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/github/license/bashu/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/travis/bashu/django-easy-maps.svg
    :target: https://travis-ci.org/bashu/django-easy-maps/

Installation
------------

Either clone this repository into your project, or install with ``pip install django-easy-maps``

You'll need to add ``easy_maps`` to ``INSTALLED_APPS`` in your project's ``settings.py`` file:

.. code-block:: python

    import django
    
    INSTALLED_APPS = (
        ...
        'easy_maps',
    )

    if django.VERSION < (1, 7):
        INSTALLED_APPS += (
            'south',
        )

Then run ``./manage.py syncdb`` to create the required database tables

Upgrading from 0.9
~~~~~~~~~~~~~~~~~~

Upgrading from 0.9 is likely to cause problems trying to apply a
migration when the tables already exist. In this case a fake migration
needs to be applied:

.. code-block:: shell

    ./manage.py migrate easy_maps 0001 --fake

Configuration (optional)
------------------------

If you need a place where center the map when no address is inserted
yet add the latitude and longitude to the ``EASY_MAPS_CENTER`` variable in
your ``settings.py`` like the following:

.. code-block:: python

    EASY_MAPS_CENTER = (-41.3, 32)

To use a custom geocoder set ``EASY_MAPS_GEOCODE`` option:

.. code-block:: python

    # Default: 'easy_maps.geocode.google_v3'
    EASY_MAPS_GEOCODE = 'example.custom_geocode'

Please see ``example`` application. This application is used to
manually test the functionalities of this package. This also serves as
a good example.

You need Django 1.4 or above to run that. It might run on older versions but that is not tested.

Usage
-----

First of all, load the ``easy_map_tags`` in every template where you want to use it:

.. code-block:: html+django

    {% load easy_maps_tags %}

Use:

.. code-block:: html+django

    {% easy_map <address> [<width> <height>] [<zoom>] [using <template_name>] %}

For example:

.. code-block:: html+django

    {% load easy_maps_tags %}

    <!-- Default map with 300x400 dimensions -->
    {% easy_map "Russia, Ekaterinburg, Mira 32" 300 400 %}

    <!-- Variable address, custom detail level and custom template -->
    {% easy_map address 200 200 5 using 'map.html' %}

The coordinates for map will be obtained using google geocoder on first
access. Then they'll be cached in DB. Django's template caching can be used
later in order to prevent DB access on each map render:

.. code-block:: html+django

    {% load easy_maps_tags cache %}

    {% cache 600 my_map firm.address %}
        {% easy_map firm.address 300 400 %}
    {% endcache %}

Templates
---------

If the default map template is not sufficient then custom map template can be
used. For example:

.. code-block:: html+django

    {% easy_map address using 'map.html' %}
    {% easy_map address 200 300 5 using 'map.html' %}

The template will have ``map`` (``easy_maps.Address`` instance
auto-created for passed address on first access), ``width``, ``height``
and ``zoom`` variables. The outer template context is passed to rendered
template as well.

You can start your own template from scratch or just override some blocks in the
default template.

Please refer to http://code.google.com/apis/maps/documentation/javascript/ for
detailed Google Maps JavaScript API help.

Widgets
-------

``django-easy-maps`` provides basic widget that displays a map under the address
field. It can be used in admin for map previews. For example:

.. code-block:: python

    from django import forms
    from django.contrib import admin

    from easy_maps.widgets import AddressWithMapWidget

    from .models import Firm

    class FirmAdmin(admin.ModelAdmin):
        class form(forms.ModelForm):
            class Meta:
                widgets = {
                    'address': AddressWithMapWidget({'class': 'vTextField'})
                }

    admin.site.register(Firm, FirmAdmin)

``address`` field should be either a ``CharField`` or ``TextField``.

Contributing
------------

If you've found a bug, implemented a feature or customized the template and
think it is useful then please consider contributing. Patches, pull requests or
just suggestions are welcome!

License
-------

``django-easy-maps`` is released under the MIT license.
