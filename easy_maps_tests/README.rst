django-easy-maps test project
=================================
Project to reproduce errors for others to debug it.

Installation
============

::

    cd easy_maps_tests
    mkvirtualenv django-easy-maps-test
    pip install -r requirements.txt
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py test
    ./manage.py runserver


