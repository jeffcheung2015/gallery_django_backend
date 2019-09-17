from .base import *
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# 'django-dev.ap-southeast-1.elasticbeanstalk.com' secret key
GOOGLE_RECAPTCHA_SECRET_KEY = '6LddeLgUAAAAAETSEErsr7dG9lJhtxFBXmFPhf7U'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}

CORS_ORIGIN_WHITELIST = (
       'http://django-dev.ap-southeast-1.elasticbeanstalk.com'
)

# AWS
from backend.secrets import (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

AWS_LOCATION = ''
AWS_STORAGE_BUCKET_NAME ='djangoreact'
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_CUSTOM_DOMAIN='%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
     'CacheControl': 'max-age=86400',
}
DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'build/static'),
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL='https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
AWS_DEFAULT_ACL = None

# elasticsearch
ELASTICSEARCH_DSL={
    'default': {
        # 'hosts': 'localhost:9200'
        'hosts': 'https://search-django-react-ft52f2ee6fdhtohze2fulmbo7y.ap-southeast-1.es.amazonaws.com/',
        'port': 9200,
        'use_ssl': True,
        'verify_certs': True,
        'http_auth': AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME, 'es'),
        'connection_class': RequestsHttpConnection
    },
}
