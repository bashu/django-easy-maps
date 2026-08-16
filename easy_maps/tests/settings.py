SECRET_KEY = "DUMMY_SECRET_KEY"  # noqa: S105

# Application definition

PROJECT_APPS = ["easy_maps.tests", "easy_maps"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.staticfiles",
    *PROJECT_APPS,
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

EASY_MAPS_GOOGLE_KEY = "AIzaSyATg_isuGSCHIlJamrxAXfkFDTYhIz7ytM"
