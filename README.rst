django-easy-maps
================

.. image:: https://img.shields.io/pypi/v/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/pypi/dm/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/github/license/bashu/django-easy-maps.svg
    :target: https://pypi.python.org/pypi/django-easy-maps/

.. image:: https://img.shields.io/travis/bashu/django-easy-maps.svg
    :target: https://travis-ci.com/github/bashu/django-easy-maps/

This app makes it easy to display a map for any given address in
django_ templates. No manual geocoding, html/js copy-pasting or Django
model changes are needed.

Maitained by `Basil Shubin <https://github.com/bashu/>`_, and some great
`contributors <https://github.com/kmike/django-easy-maps/contributors>`_.

Installation
------------

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install django-easy-maps

Setup
-----

You'll need to add ``easy_maps`` to ``INSTALLED_APPS`` in your project's ``settings.py`` file:

.. code-block:: python

    INSTALLED_APPS += [
        'easy_maps',
    ]

Then run ``./manage.py migrate`` to create the required database tables.

Configuration
-------------

The only mandatory configuration is the ``EASY_MAPS_GOOGLE_KEY`` variable:

.. code-block:: python

    EASY_MAPS_GOOGLE_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ___0123456789'

If you need a place to center the map at when no address is inserted
yet, add the latitude and longitude to the ``EASY_MAPS_CENTER`` variable in
your ``settings.py`` like the following:

.. code-block:: python

    EASY_MAPS_CENTER = (-41.3, 32)

Other optional settings:

.. code-block:: python

    # Optional
    EASY_MAPS_ZOOM = 8  # Default zoom level, see https://developers.google.com/maps/documentation/javascript/tutorial#MapOptions for more information.
    EASY_MAPS_LANGUAGE = 'ru'  # See https://developers.google.com/maps/faq#languagesupport for supported languages.

Please see the ``example`` application. This application is used to
manually test the functionalities of this package. This also serves as
a good example.

You need Django 1.8 or above to run that. It might run on older versions but that is not tested.

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
    {% easy_map address 200 200 5 using "map.html" %}

The coordinates for map will be obtained using google geocoder on first
access. Then they'll be cached in DB. Django's template caching can be used
later in order to prevent DB access on each map render:

.. code-block:: html+django

    {% load easy_maps_tags cache %}

    {% cache 600 my_map firm.address %}
        {% easy_map firm.address 300 400 %}
    {% endcache %}

Templates
~~~~~~~~~

If the default map template is not sufficient then a custom map template can be
used. For example:

.. code-block:: html+django

    {% easy_map address using "map.html" %}
    {% easy_map address 200 300 5 using "map.html" %}

The template will have ``map`` (``easy_maps.Address`` instance
auto-created for passed address on first access), ``width``, ``height``
and ``zoom`` variables. The outer template context is passed to the rendered
template as well.

You can start your own template from scratch or just override some blocks in the
default template.

Please refer to https://developers.google.com/maps/documentation/javascript/ for
detailed Google Maps JavaScript API help.

Widgets
~~~~~~~

``django-easy-maps`` provides a basic widget that displays a map under the address
field. It can be used in the admin for map previews. For example:

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

Credits
-------

`django-easy-maps <https://github.com/bashu/django-easy-maps/>`_ was originally started by `Mikhail Korobov <http://kmike.ru/>`_ who has now unfortunately abandoned the project.

License
-------

``django-easy-maps`` is released under the MIT license.

.. _django: https://www.djangoproject.com
