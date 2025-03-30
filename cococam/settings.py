from pathlib import Path

import os
import stripe
import django
from django.utils.encoding import smart_str
from django.dispatch import Signal
from datetime import timedelta as timedelta
import certifi
import stripe
import django.dispatch
import pymysql

import ssl
import django.dispatch
# import environ



context = ssl._create_unverified_context()

ssl_context = ssl.create_default_context(cafile=certifi.where())
EMAIL_SSL_CERTFILE = certifi.where()

# env = environ.Env()
# environ.Env.read_env()

pymysql.install_as_MySQLdb()
pizza_done = django.dispatch.Signal()
stripe.ca_bundle_path = certifi.where()
# Инициализация Stripe после установки пути
stripe.api_key = "sk_test_51QkVEiQ0v0qwOsT6CA7ADNdlZV86e2dvKPUF8cCtEpsxIenN6cL2J67oQ1cexYf2jZlF0ijw0mK200mPV4DE30"
model_delete_signal = Signal()
model_delete_signal.send(sender='session_delete')
django.utils.encoding.smart_text = smart_str

stripe.verify_ssl_certs = False

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-3@m9gm0mf_9q=3wd=p1(#mmd_doyp0$k1e+=ep"

DEBUG = True

ALLOWED_HOSTS = ['*']


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/'

STRIPE_LIVE_MODE = False  # Переключите на True для продакшена
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# STRIPE_WEBHOOK_SECRET = ""
STRIPE_WEBHOOK_SECRET = "whsec_c9bff96b414e5c8c77ed131779abe6c78758e34b173c09543f4"
STRIPE_TEST_PUBLIC_KEY = 'pk_test_51QkVEAZa9CN0SaNx6WigSag5wWD1Jh6kyWJm6BMXXYFR2pUjPB0QmHNUP8FM7n5kxnV878Ieecur6005etaGyp3'
STRIPE_TEST_SECRET_KEY = 'sk_test_51QkTGf3hv0qwOsT6CA7ADNdlZV86e2dvKPUF8cCtEpsxIenN6cL2J67oQ1cexYf2jZlF0ijw0mK200mPV4DE30'
STRIPE_LIVE_MODE = False  # Change to True in production
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "core",
    "dashboard",
    "link",
    "djstripe",
    "corsheaders",
    "payments",
    
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
]



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'accounts.middleware.JWTAuthenticationMiddleware',
]

# Настройки CSRF
CSRF_COOKIE_SECURE = False  # Для разработки
CSRF_COOKIE_HTTPONLY = False  # Для доступа через JS
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Настройки CORS (если используется)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS



ROOT_URLCONF = "cococam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.csrf',
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cococam.wsgi.application"



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'cococam3',
#         'USER': 'admin_cococam',
#         'PASSWORD': 'pad',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cococam3',
        'USER': 'root',
        'PASSWORD': 'root',
        'PORT': '',
        'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
    }
}





# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]




REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,                  # обновлять refresh-токен автоматически
    'BLACKLIST_AFTER_ROTATION': True,               # Добавлять старые токены в черный список
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',                           # Алгоритм подписи токена
    'SIGNING_KEY': SECRET_KEY,                      # Ключ для подписи токена
    'VERIFYING_KEY': None,                          # Ключ для проверки токена (если используется асимметричный алгоритм)
    'AUTH_HEADER_TYPES': ('Bearer',),               # Тип заголовка для аутентификации
    'USER_ID_FIELD': 'id',                          # Поле для идентификации пользователя
    'USER_ID_CLAIM': 'user_id',                     # Поле в токене для идентификации пользователя
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),   
}



# Настройки для кук
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False

# CORS настройки
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']


SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Или 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 3600  # 1 час - синхронизировать с ACCESS_TOKEN_LIFETIME
SESSION_SAVE_EVERY_REQUEST = True 
SESSION_COOKIE_SECURE = not DEBUG  # Для разработки, в production должно быть True
SESSION_COOKIE_HTTPONLY = True  # Защита от XSS
SESSION_COOKIE_SAMESITE = 'Lax'  # Защита от CSRF

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

# DJOSER
DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'TOKEN_MODEL': None,  # We use only JWT
    'ACTIVATION_URL': 'auth/users/activation/{uid}/{token}/',
    # 'SEND_CONFIRMATION_EMAIL': True,  # Отправлять письмо с подтверждением регистрации
    # 'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,  # Показывать ошибку, если email не найден
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',  # Локальный кэш в памяти
    }
}


EMAIL_BACKEND = 'cococam.custom_email_backend.CustomEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'gmail.com'
EMAIL_HOST_PASSWORD = 'yjidry'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False



LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
