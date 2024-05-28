from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--^t_hu$o8hc8kh#h!_6*o*ufr6w-c8(9l4j&96=g2@^72-rfon'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['smart-algo.in','www.smart-algo.in','https://smart-algo.in','https://www.smart-algo.in','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "ash",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'trade',
    'stratergy',
    'alerts',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'allauth.account.middleware.AccountMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'trading.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'trade.context_processors.custom_admin_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]
handler404 = 'trade.views.handler404'
WSGI_APPLICATION = 'trading.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
#    'allauth.account.auth_backends.AuthenticationBackend',
]


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_URL="/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# STATICFILES_DIRS =[
#     os.path.join(BASE_DIR, "static"),
# ]

CSRF_TRUSTED_ORIGINS = [
    'https://smart-algo.in',
    'https://www.smart-algo.in',
    'http://127.0.0.1:8000',
]


MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}



SITE_ID=1
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_REDIRECT_URL = "/dashboard"
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = "/login"
LOGIN_URL = '/accounts/google/login/'

#SOCIALACCOUNT_PROVIDERS = {
#    'google': {
#        'APP': {
#            'client_id': '557775205514-da83ci03vvnq6p235h8kjak4o1a6flga.apps.googleusercontent.com',
#            'secret': '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',
#            'key': ''
#        }
#    }
#}

UPI_TOKEN = "83cc9cbe167cd77dc5328f87dbb7868f"

# CELERY_broker_url = 'redis://localhost:6379/0'
# result_backend = 'redis://localhost:6379/0'


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '531414445013-esrqk4lkniqmp6u78898hooc2ej7ohtf.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'


ASH_SITE_HEADER =  getattr(settings, 'ASH_SITE_HEADER', 'Smart-algo Admin')
ASH_SITE_LOGO_ICON = getattr(settings, 'ASH_SITE_LOGO_ICON', 'icon-database')



