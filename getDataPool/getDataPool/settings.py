"""
Django settings for getDataPool project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import time
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3vvhl@iw_cohr@=ncsx)+oeof^*%-d_nujvenhq3*=50)d3&mg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_apscheduler',
    'web_apscheduler'
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

ROOT_URLCONF = 'getDataPool.urls'

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

WSGI_APPLICATION = 'getDataPool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'django',
    'USER':'root',
    'PASSWORD':'djangotest',
    'PORT':3306,
    'HOST':'127.0.0.1',
    'CHARSET':'utf8'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#log porties
LOG_PATH = BASE_DIR / "logs"

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        # 日志格式
        "standard": {"format": "%(asctime)s [%(levelname)s] %(filename)s::%(funcName)s:%(lineno)d: %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},  # 简单格式
    },
    # 过滤
    "filters": {},
    # 定义具体处理日志的方式
    "handlers": {
        # 默认记录所有日志
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / f'system-{time.strftime("%Y-%m-%d")}.log',
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / f'error-{time.strftime("%Y-%m-%d")}.log',
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码
        },
        # 控制台输出
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    # 配置用哪几种 handlers 来处理日志
    "loggers": {
        # 类型 为 django 处理所有类型的日志， 默认调用
        "django": {
            "level": "INFO",
            "handlers": ["default", "console"],
            "propagate": False,
        },
        # log 调用时需要当作参数传入
        "log": {
            "level": "INFO",
            "handlers": ["error", "console", "default"],
            "propagate": True,
        },
    },
}