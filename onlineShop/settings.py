"""
Django settings for onlineShop project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
from datetime import  timedelta
import environ
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
env = environ.Env(
    DEBUG=(bool, False)  # Set default values and casting types
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=6jpua_blme+)2591*ale$v^kwv168)3hcug&tru0t&g8(m4bp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'category',
    'store',
    'cart',
    'cms',
    "orders",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware must be before CorsMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Make sure CORS middleware comes after AuthenticationMiddleware
]

ROOT_URLCONF = 'onlineShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.categories_list',
                'cart.context_processors.cart_items_count',
            ],
        },
    },
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://onlineshopcosmetics.netlify.app",
    # add any other domains you want to allow
]

# Cookie settings
if env("ENV") == "prod":  # Assuming you have ENV set to "prod" for production
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'Lax'  # Adjust if cross-site requests are necessary
    SESSION_COOKIE_SAMESITE = 'Lax'  # Adjust if cross-site requests are necessary
else:
    CSRF_COOKIE_SECURE = False      # Use False for local development
    CSRF_COOKIE_SAMESITE = 'Lax'   # Same as above
    SESSION_COOKIE_SECURE = False  # Set to True in production to ensure it's sent over HTTPS

SESSION_COOKIE_NAME = 'sessionid'  # Default session cookie name
SESSION_COOKIE_HTTPONLY = False  # Prevent JavaScript access to the cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # Adjust as necessary (Lax or None for cross-site)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600  # Two weeks


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Adjust this to the desired number of items per page
    
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_BLACKLIST': 'rest_framework_simplejwt.token_blacklist.models.BlacklistedToken',
}

WSGI_APPLICATION = 'onlineShop.wsgi.application'

AUTH_USER_MODEL= 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR /'static'

STATICFILES_DIRS=[
    'onlineShop/static',
]

MEDIA_URL='/media/'
MEDIA_ROOT=BASE_DIR /'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGES_TAGS = {
    messages.ERROR:'danger',
   
}



DEBUG = env("DEBUG")
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
