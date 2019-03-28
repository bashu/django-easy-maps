#!/usr/bin/env python

import os
import re
import sys
import codecs

from setuptools import setup, find_packages


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    os.chdir('easy_maps')
    try:
        from django.core import management
        management.call_command('compilemessages', stdout=sys.stderr, verbosity=1)
    except ImportError:
        if 'sdist' in sys.argv:
            raise
    finally:
        os.chdir('..')


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-easy-maps',
    version=find_version('easy_maps', '__init__.py'),
    license='MIT License',

    install_requires=[
        'django-classy-tags>=0.6.2',
        'django-appconf',
        'geopy>=0.96',
    ],
    requires=[
        'Django (>=1.4.2)',
    ],

    description="This app makes it easy to display a map for a given address",
    long_description=read('README.rst'),

    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    maintainer='Basil Shubin',
    maintainer_email='basil.shubin@gmail.com',

    url='https://github.com/bashu/django-easy-maps',
    download_url='https://github.com/bashu/django-easy-maps/zipball/master',

    packages=find_packages(exclude=('example*', '*.tests*')),
    include_package_data=True,

    tests_require=[
        'django-setuptest',
        'mock',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
