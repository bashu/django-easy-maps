import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from easy_maps import __version__

setup(
    name='django-easy-maps',
    version=__version__,
    packages=[
        'easy_maps',
        'easy_maps.migrations',
        'easy_maps.templatetags',
        'easy_maps.south_migrations',
    ],
    include_package_data=True,
    license='MIT License',
    description="This app makes it easy to display a map for a given address",
    long_description=README,
    url='https://github.com/kmike/django-easy-maps',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',
    maintainer='Basil Shubin',
    maintainer_email='basil.shubin@gmail.com',
    install_requires=[
        'django',
        'django-appconf',
        'django-classy-tags==0.6.2',
        'geopy>=0.96',
    ],    
    classifiers=[
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
    zip_safe=False,
)
