import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, '..')))

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
    }
}
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)


STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'static'))

INSTALLED_APPS=(
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'easy_maps',
    'test_app',
#    'devserver',
    'south'
)
