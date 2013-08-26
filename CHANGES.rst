0.8.3 (2013-08-27)
------------------

- ``easy_map`` tag now works when address is None.

0.8.2 (2013-07-02)
------------------

- Unique constraint is added to Address.address field (to prevent
  MultipleObjectsReturned exceptions).

  In order to upgrade, run

      python manage.py migrate easy_maps

- German translation is added.

0.8.1 (2013-03-25)
------------------

- Fix regressions in geocoding errors handling introduced in 0.8.

0.8 (2013-03-24)
----------------

- Testing improvements;
- EASY_MAPS_CENTER setting for default map coordinates;
- allow to pass an Address instance as argument of easy_map tag;
- better error handling;
- switch to GoogleV3 geocoder;
- customization hook: it is now possible to use a custom geocoding method;
- EASY_MAPS_GOOGLE_KEY now does nothing (it is not a meaningful option
  for V3 Geocoding API).

Minimum required django version is 1.3 since this release.
It may work with older versions, but this is untested.

0.7.4 (2013-01-03)
------------------

- switch to https;
- make example settings django 1.4 compatible;

0.7.3 (2012-09-21)
------------------

- use only first placemark from geocoder.

0.7.2 (2012-01-07)
------------------

- static fallback for map.html;
- fix localization of floats.

0.7.1 (2011-01-31)
------------------

- better error handling;
- EASY_MAPS_GOOGLE_KEY setting.

0.7 (2010-12-24)
----------------

- longtitude -> longitude;
- display is fixed for comma-delimited float locales.

0.6 (2010-12-02)
----------------

- admin preview widget;
- bugfixes.

0.5 (2010-12-01)
----------------

Initial release
