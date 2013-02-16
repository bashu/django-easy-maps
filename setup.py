#!/usr/bin/env python
from distutils.core import setup
version='0.7.4'

setup(
    name = 'django-easy-maps',
    version = version,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'https://bitbucket.org/kmike/django-easy-maps/',

    description = 'This app makes it easy to display a map for a given address.',
    long_description = open('README.rst').read() + '\n\n' + open('CHANGES.rst').read(),
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
