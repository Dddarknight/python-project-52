from pathlib import Path
import dj_database_url
import os
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent


IS_HEROKU = "DYNO" in os.environ

if not IS_HEROKU:
    DEBUG = True


if IS_HEROKU:
    ALLOWED_HOSTS = ['webserver', "*"]
else:
    ALLOWED_HOSTS = ['webserver', '127.0.0.1']

SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "bootstrap4",
    'task_manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'

if IS_HEROKU:
    DATABASE_URL = 'postgresql://<postgresql>'
else:
    DATABASE_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOOTSTRAP4 = {
    "css_url": {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/"
                "dist/css/bootstrap.min.css",
        "integrity": "sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0Ej"
                     "AuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn",
        "crossorigin": "anonymous",
    },

    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/"
               "dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjs"
                     "OMm/tB9LTS58ONXgqbR9W8oWht/amnpF",
        "crossorigin": "anonymous",
    },

    "theme_url": "https://getbootstrap.com/docs/4.4/examples/cover/cover.css",

    "jquery_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.min.js",
        "integrity": "sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/"
                     "6Z/hRTt8+pR6L4N2",
        "crossorigin": "anonymous",
    },

    "jquery_slim_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "integrity": "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+Ibb"
                     "VYUew+OrCXaRkfj",
        "crossorigin": "anonymous",
    },

    'javascript_in_head': False,

    'include_jquery': False,

    'horizontal_label_class': 'col-md-3',

    'horizontal_field_class': 'col-md-9',

    'set_placeholder': True,

    'required_css_class': '',

    'error_css_class': 'is-invalid',

    'success_css_class': 'is-valid',

    'formset_renderers': {
        'default': 'bootstrap4.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap4.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap4.renderers.FieldRenderer',
        'inline': 'bootstrap4.renderers.InlineFieldRenderer',
    },
}

LOCALE_PATHS = [
    'locale',
]
