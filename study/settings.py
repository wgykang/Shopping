"""
Django settings for study project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l+8-=8v1%6d+9+my+=)y0e1a&9*84r-_#o159c^i8$1gyj_rl%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',
    'DjangoUeditor',  # 富文本
    'crispy_forms',
    'django_filters',
    'xadmin',  # xadmin后台管理
    'rest_framework',
    'corsheaders',  # 后端解决跨域请求
    'rest_framework.authtoken',  # token认证
    'social_django',  # 第三方登录
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域请求
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # 跨域
ROOT_URLCONF = 'study.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # 第三方登录
                'social_django.context_processors.login_redirect',  # 第三方登录
            ],
        },
    },
]

WSGI_APPLICATION = 'study.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxshop',
        'USER': 'root',
        'HOST': '203.195.162.142',
        # 'HOST': 'localhost',
        'PASSWORD': '123456',
        'PORT': 3306,
        'CHARSET': 'utf8',
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"},
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# 设置时区
LANGUAGE_CODE = 'zh-hans'  # 中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False  # 默认是true，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！

# 自定义用户验证
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',  # 自定义用户验证
    'social_core.backends.weibo.WeiboOAuth2',  # 微博登录
    'social_core.backends.qq.QQOAuth2',  # qq登录
    'social_core.backends.weixin.WeixinOAuth2',  # 微信登录
    'django.contrib.auth.backends.ModelBackend',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
# 如果静态文件访问不到 肯定这里有问题
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

"""
分页
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    
}
"""
# token验证
REST_FRAMEWORK = {
    # 相当于middleware
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  全局配置时候当token过期时回返回错误,无法访问公有资源
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',  全局配置时候当token过期时回返回错误,无法访问公有资源
    ),
    # 限速的两个类
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',  # 未登录情况下,通过ip(匿名用户限速)
        'rest_framework.throttling.UserRateThrottle'  # 登录情况下通过session和token(登录用户限速)
    ),
    # 限速规则
    'DEFAULT_THROTTLE_RATES': {
        'anon': '200/minute',  # 1分钟2次
        'user': '300/minute'
    }
}

# jet设置
import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 过期时间
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^17[63]\d{8}$|^150\d{8}$"

# 云片网设置
APIKEY = "ca31d1414fab8f9a5351e62a0e87e721"

# 支付宝相关配置
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/siyao_2048.txt')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_2048.txt')

# 缓存时间drf-extensions

REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 10*60,
}
# django-redis缓存配置
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# 第三方登录secret和key配置
SOCIAL_AUTH_WEIBO_KEY = '432622721'  # 微博
SOCIAL_AUTH_WEIBO_SECRET = "1d62d78ddc2686076506d5194c4ad50d"

SOCIAL_AUTH_QQ_KEY = 'foobar'  # QQ
SOCIAL_AUTH_QQ_SECRET = 'bazqux'

SOCIAL_AUTH_WEIXIN_KEY = 'foobar'  # 微信
SOCIAL_AUTH_WEIXIN_SECRET = 'bazqux'

# 第三方登录成功后跳转的url
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index/'