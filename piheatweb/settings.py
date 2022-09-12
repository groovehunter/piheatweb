import os
from piheatweb.util import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = BASE_DIR + '/log'
TMPPATH = BASE_DIR + '/tmp/'

#DEBUG =True
DEBUG =False
DEBUG2=False
logfn_debug = LOG_DIR + '/debug.log'
logfn_piheat= LOG_DIR + '/piheat.log'
logfn_django= LOG_DIR + '/django.log'
logfn_root  = LOG_DIR + '/root.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname}| {module},{lineno} - {message}',
            'style': '{',
            'datefmt': '%H:%M:%S',
        },
        'simple': {
            'format': '{levelname}| {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_root': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_root,
            'formatter': 'verbose',
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_django,
            'formatter': 'simple',
        },
        'file_piheat': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_piheat,
            'formatter': 'verbose',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logfn_debug,
            'formatter': 'verbose',
        },
       'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file_root'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file_django'],
            'level': 'INFO',
            'propagate': False,
        },
        'motors.rules': {
            'handlers': ['file_piheat'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'motors.views': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'asyncio': { 'level': 'WARNING', },
        'faker.factory': { 'level': 'WARNING', },
    },
}
"""
"""

SECRET_KEY = '&a1h1h2+=m(l34j40z#_!e$4p2qdw4jy%-zv3s@hna0(*7$civ'

AUTH_USER_MODEL = "users.CustomUser"
TAILWIND_APP_NAME = 'theme'
DJANGO_TABLES2_TEMPLATE = "table.html"

ALLOWED_HOSTS = ['raspberrypi', 'piheat', 'localhost', 'piheatdev', 'groove.selfhost.eu']

# Application definition

INSTALLED_APPS = [
    'piheatweb.apps.PiheatwebConfig',
    'sensors.apps.SensorsConfig',
    'motors.apps.MotorsConfig',
    'cntrl.apps.CntrlConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'tailwind',
    'theme',
    'py_yaml_fixtures',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'login_required.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOGIN_REQUIRED_IGNORE_PATHS = [
    r'/users/logout/$'
    r'/users/login/$',
    r'/admin/$',
    r'/admin/login/$',
    r'/about/$'
]

ROOT_URLCONF  = 'piheatweb.urls'
MENU_CONF     = 'piheatweb/menu.yaml'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': ['piheatweb/templates'],
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

WSGI_APPLICATION = 'piheatweb.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'piheat_db',
        'USER': 'piheat',
        'PASSWORD': 'ppp',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/users/login'
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"), )
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
