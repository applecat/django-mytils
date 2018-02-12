SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    "mytils",
    "tests",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # TODO: Test with this True!
# USE_TZ = True  # ValueError: localtime() cannot be applied to a naive datetime
