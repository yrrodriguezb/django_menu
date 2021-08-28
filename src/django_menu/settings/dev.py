from .base import *

DEBUG = True 

ALLOWED_HOSTS = []

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Applications 

INSTALLED_APPS = DJANGO_APPS + APPS_THIRD_PARTY + APPS