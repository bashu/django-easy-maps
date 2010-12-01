import os, sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_ROOT, '..')))

DEBUG = True
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'db.sqlite'
ROOT_URLCONF = 'urls'
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

INSTALLED_APPS=(
    'easy_maps',
    'test_app',
#    'devserver',
    'south'
)
