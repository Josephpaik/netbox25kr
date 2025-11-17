###################################################################
#  This file serves as a base configuration for testing purposes  #
#  only. It is not intended for production use.                   #
###################################################################

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netbox',
        'USER': 'netbox',
        'PASSWORD': 'netbox1234!',  # 2.2단계에서 설정한 비밀번호
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 300,
    }
}

PLUGINS = [
    'netbox.tests.dummy_plugin',
]

REDIS = {
    'tasks': {
        'HOST': 'localhost',
        'PORT': 6379,
        'USERNAME': '',
        'PASSWORD': '',
        'DATABASE': 0,
        'SSL': False,
    },
    'caching': {
        'HOST': 'localhost',
        'PORT': 6379,
        'USERNAME': '',
        'PASSWORD': '',
        'DATABASE': 1,
        'SSL': False,
    }
}

SECRET_KEY = 'LX=UhyrVjhBMZprNtpMp+hgSM(D64lc1(J$YBV%iGMqtt*gPU)YZ0123456789'
                          
DEFAULT_PERMISSIONS = {}

ALLOW_TOKEN_RETRIEVAL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True
}

DEBUG = True

TIME_ZONE = 'Asia/Seoul'

