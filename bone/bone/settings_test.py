from .settings import *

SECRET_KEY = 'test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bone',
    }
}

import fakeredis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://",
        "OPTIONS": {
            "REDIS_CLIENT_CLASS": "fakeredis.FakeStrictRedis",
        }
    }
}
