import django

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = (
    'easy_maps',
)
if django.VERSION < (1, 7):
    INSTALLED_APPS += (
        'south',
    )
