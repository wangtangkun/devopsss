"""
Django settings for xitong project.

Generated by 'django-admin startproject' using Django 1.11.21.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qtgkkt65lvs+fywu+8_2^q3w&7$cvp$0i*9!0wy9uz8fepm8&9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.auth.AuthenticationMiddleware',
]

ROOT_URLCONF = 'xitong.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'xitong.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'xt',
        'HOST':'192.168.31.212',
        # 'HOST':'127.0.0.1',
        'PORT':3306,
        'USER':'root',
        'PASSWORD':'1234',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LOGGING = {
#     "version": 1,  # 保留字段,不能变
#     "disable_existing_loggers": False,  # 是否禁用已经存在的日志实例(django自带的报错),一般不禁用.
#
#     # 一条日志记录需要以文本的形式展现出来，Formatters定义了文本的格式。一个格式化器一般由python的格式字符串组成。不过，你也可以自定义格式。
#     "formatters": {  # 用来记录日志的输出格式
#         "default": {  # 名字随便定义（默认的输出格式）。上面图片里的格式都可以应用，分隔符|也可以随便定义成别的
#             "format": '%(levelname)s|%(asctime)s|%(module)s|%(lineno)d|%(message)s'
#         },
#         "simple": {  # 名字随便定义（简单的输出格式）。上面图片里的格式都可以应用，分隔符|也可以随便定义成别的
#             "format": '%(asctime)s|%(levelname)s|%(message)s'
#         }
#     },
#
#     'filters': {  # 定义日志的过滤器，一般不修改
#         'require_debug_true': {  # （名字随便定义）   # 只有在setting中的 DEBUG = True 的时候才会生效
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#
#     # handler是实际上来处理日志记录的地方。它说明的是一个特殊的记录行为，比如，将这个信息写在屏幕上、写到一个文件或者写到一个Network socket中去。这一点是通过handler的class属性来配置的。
#     # 与logger一样，handler也有日志级别（level）属性，如果logger传来的记录级别没有handler高，那么这条记录也会被忽略。
#
#     # 为什么logger和handler都要设置level？
#     # 因为一个logger可以有多个handler，且每个handler可以有不同的log level。这样一来，一个logger可以接受一类日志的多个级别的信息，并且将不同级别的信息进行不同的处理。
#
#
#     "handlers": {  # 定义日志的详细格式
#         "console": {
#             "level": "DEBUG",  # 触发日志级别
#             "formatter": "simple",  # 使用简单输出格式
#             'class': 'logging.StreamHandler',  # 用来定义日志的切分格式
#             # 'logging.handlers.RotatingFileHandler' 按照大小来切割（比如定义日志超过50M就切分）   日志格式：日志文件名-数字
#             # 'logging.handlers.TimedRotatingFileHandler'  按照时间\日期来切割     日志格式：日志文件名-日期
#             'filters': ['require_debug_true'],  # 只有在debug=True的时候才会在屏幕上显示内容
#         },
#         "admin": {
#             "level": "INFO",  # 触发日志级别
#             "formatter": "default",  # 使用默认输出格式
#             'class': 'logging.handlers.RotatingFileHandler',  # 按照日志大小切分
#             "filename": "/var/log/issue.log",  # 日志位置、日志文件名
#             "maxBytes": 1024 * 1024 * 10,  # 日志的大小  10Mb（超过这个大小则分割）
#             "encoding": "utf-8",  # 编码格式
#             "backupCount": 5  # 最多保留5份日志
#         },
#         "error": {
#             "level": "ERROR",  # 触发日志级别
#             "formatter": "default",
#             'class': 'logging.handlers.TimedRotatingFileHandler',  # 按照时间来切分
#             "filename": "/var/log/issue.error",
#             "when": "D",  # 每天一切， 可选值有S/秒 M/分 H/小时 D/天 W0-W6/周(0=周一) midnight/如果没指定时间就默认在午夜0点
#             "encoding": "utf-8"
#         }
#     },
#
#     # Loggers中的logger是整个日志机制的入口，一个logger对应一种类型的日志。logger通过设定日志级别（level属性），来配置logger的触发条件。Python中定义了5种日志级别：
#     # 由低到高分别为：DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL。
#     # 代码中通过 logger = logging.getLogger('django') 获得一个logger的实例，’django’是一种类型的日志。
#     # 当一条日志信息发给logger时，日志信息的log level会和logger的log level对比。如果日志信息的log level达到或者是超过logger的log level的级别，这条信息会被发往handler去处理。否则，这条信息会被忽略。一旦logger决定信息要进一步被处理，这条信息会被传给给Handler（logger的handler属性）.
#     # 所以，logger更像是一个日志处理的分发器。
#
#     "loggers": {  # 日志处理的分发器
#         "django": {  # 名字随便定义
#             "handlers": ["console", "admin"],  # 调用handlers 里的console 和 admin
#             "level": "DEBUG"  # 触发日志级别
#         },
#         "default": {  # 名字随便定义
#             "handlers": ["admin", "error"],  # 调用handlers 里的admin 和 error
#             "level": "INFO",  # 触发日志级别
#             'propagate': True,  # 是否向上一级logger实例传递日志信息
#         }
#     }
# }
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

git_path="/updata/git/"


STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]