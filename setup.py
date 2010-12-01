#!/usr/bin/env python
from distutils.core import setup
version='0.5.3'

setup(
    name = 'django-easy-maps',
    version = version,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'http://bitbucket.org/kmike/django-easy-maps/',
    download_url = 'http://bitbucket.org/kmike/django-easy-maps/get/tip.zip',

    description = 'This app makes it easy to display a map for a given address.',
    long_description = open('README.rst').read(),
    license = 'MIT license',
    requires = ['django (>=1.0)', 'geopy'],

    packages=['easy_maps', 'easy_maps.templatetags', 'easy_maps.migrations'],
    package_data={'easy_maps': ['templates/easy_maps/*']},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
