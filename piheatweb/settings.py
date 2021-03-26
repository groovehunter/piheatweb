
import os
from piheatweb.util import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = BASE_DIR + '/log'
TMPPATH = BASE_DIR + '/tmp/'
DEBUG2=False

SECRET_KEY = '&a1h1h2+=m(l34j40z#_!e$4p2qdw4jy%-zv3s@hna0(*7$civ'

DEBUG = True
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
if IS_PC:
  logfn = os.environ['HOME'] + '/log/debug.log'
if IS_RPi:
  #logfn = os.environ['HOME'] + '/log/debug.log'
  logfn = '/home/pi/pw/log/debug.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': logfn,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
"""
"""
