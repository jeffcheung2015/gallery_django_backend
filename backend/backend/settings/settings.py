from .base import *



# SECURITY WARNING: keep the secret key used in production secret!
# localhost secret key
GOOGLE_RECAPTCHA_SECRET_KEY = '6LcpqLUUAAAAAFUg1rAzd_pxPSr2-2rsAl4kfU3F'


STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "build/static"),
    os.path.join(BASE_DIR, "media/static"),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# for dev react purpose
CORS_ORIGIN_WHITELIST = (
       # this is for react dev server one
       'http://127.0.0.1:3000',
       'http://localhost:3000',
       # this is for built react one
       'http://127.0.0.1:8000',
       'http://localhost:8000',
)

# elasticsearch
ELASTICSEARCH_DSL={
    'default': {
        'hosts': 'localhost',
        'port': 9200,
    },
}
