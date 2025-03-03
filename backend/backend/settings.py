"""
Django settings for backend project.
"""

from pathlib import Path
import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
import logging

# ✅ Layihənin əsas qovluq yolu
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Gizli açar (Production üçün ENV dəyişənlərindən istifadə edin)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-i&l0sp&h*oxwdu9q8vafl8@fyq0zgj$absme12kui0q%g75wfb')

# ✅ Debug rejimi (Production-da `False` olmalıdır)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# ✅ İcazə verilən hostlar
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ✅ Quraşdırılmış tətbiqlər (Apps)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 📌 3-cü tərəf tətbiqlər
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',

    # 📌 Özel tətbiqlər
    'backend.accounts',
    'tours',
]

# ✅ İstifadə olunan dilləri qeyd edirik
LANGUAGES = [
    ('en', _('English')),
    ('az', _('Azərbaycan')),
    ('ru', _('Русский')),
    ('tr', _('Türkçe')),
]

# ✅ Default dil
LANGUAGE_CODE = 'az'

# ✅ Lokalizasiya fayllarının saxlanma yeri
LOCALE_PATHS = [BASE_DIR / 'locale/']

USE_I18N = True
USE_L10N = True
USE_TZ = True

# ✅ Middleware (Orta qat)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ URL Konfiqurasiyası
ROOT_URLCONF = 'backend.urls'

# ✅ Şablon (Template) Ayarları
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'tours/templates'],
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

# ✅ WSGI tətbiqi (Deployment üçün)
WSGI_APPLICATION = 'backend.wsgi.application'

# ✅ Verilənlər bazası (Database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Şifrə doğrulaması
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Statik fayllar (CSS, JS, şəkillər)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Media Faylları (Şəkillər və s.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'

# ✅ Django REST Framework Ayarları
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
    },
}

# ✅ JWT Token Ayarları
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
}

# ✅ CORS Ayarları
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React üçün
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Django API üçün
        "http://127.0.0.1:8000",
]
CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF Mühafizəsi aktiv edildi
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ✅ Email Ayarları
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'youremail@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'yourpassword')

# ✅ Logging Ayarları
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'backend_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
