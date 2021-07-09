"""
Django settings for hrunmanage project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import datetime
from pathlib import Path
from config import Config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9wcwawkxkr(&47ms=g2!xos^8%uzm5r-3gn*a@ut^5dp8!#$xq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = Config.DEBUG

ALLOWED_HOSTS = Config.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'django_python3_ldap',
    'django_filters',
    'demo',
    'manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls.base'

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

WSGI_APPLICATION = 'hrunmanage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if Config.DATABASE["engine"] == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': Config.DATABASE["dbname"],
            'USER': Config.DATABASE["user"],
            'PASSWORD': Config.DATABASE["password"],
            'HOST': Config.DATABASE["host"],
            'PORT': Config.DATABASE["port"],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

if Config.CACHE:

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": 'redis://:%s@%s:%s/0' % (Config.REDIS["password"], Config.REDIS["host"], Config.REDIS["port"]),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        "session": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": 'redis://:%s@%s:%s/1' % (Config.REDIS["password"], Config.REDIS["host"], Config.REDIS["port"]),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

########### LDAP AUTH ###############
if Config.AUTH_LDAP:
    AUTHENTICATION_BACKENDS = (
        'django_python3_ldap.auth.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    LDAP_AUTH_URL = Config.LDAP['host']
    LDAP_AUTH_BIND_DN = Config.LDAP['bind_dn']
    LDAP_AUTH_BIND_PASSWORD = Config.LDAP['password']
    LDAP_AUTH_SEARCH_BASE = Config.LDAP['base_dn']
    # The LDAP class that represents a user.
    LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

    LDAP_AUTH_USER_FIELDS  = {
        "username": "uid",
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail"
    }

    LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"
    LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"
    LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"
    LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"

############ log ################

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            # logging handler that outputs log messages to terminal  
            'class': 'logging.StreamHandler',
            'level': Config.LEVEL,  # message level to be written to console
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': Config.LEVEL,
            # django also has database level logging  
        },
        'django_auth_ldap': {
            'handlers': ['console'],
            'propagate': True,
            'level': Config.LEVEL,
        },
    },
}



# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# rest_framework 配置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 默认查找
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # 默认分页设置
    'DEFAULT_PAGINATION_CLASS': 'utils.page.CustomPagination',
    # 'PAGE_SIZE': 20
    'EXCEPTION_HANDLER':'utils.common.custom_exception_handler', #使用自定义异常处理
}

# JWT 相关配置
JWT_AUTH = {
    # 修改默认 JWT 前缀
    'JWT_AUTH_HEADER_PREFIX': 'token',
    # 无操作过期时间
    'JWT_LEEWAY': 300,
    # token 过期时间
    'JWT_EXPIRATION_DELTA':  datetime.timedelta(days=7),

}