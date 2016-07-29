import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'wzja%jekbfa2as(knu&enghau%rudx(5uo0_mik7%ph%d$&fvk'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zfwechat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware'
)

ROOT_URLCONF = 'edulnwechat.urls'

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

WSGI_APPLICATION = 'edulnwechat.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        #'ENGINE': 'django.db.backends.mysql',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'USER':'root',
        #'PASSWORD':'123321',
        #'NAME':'test',
        'HOST':'127.0.0.1'
    }
}



LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'

TEMPLATE_DIRS = (
                    os.path.join(os.path.dirname(__file__), 'templates'),
                )
DEFAULT_CHARSET = "UTF-8"
 
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
) 

# ADMINS = (
#     ('wei', '784567806@qq.com'),
# )

# MANAGERS = (
#     ('wei', '784567806@qq.com'),
# )


# ============= EMAIL ==============
SERVER_EMAIL = '18312801131@163.com'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = '18312801131@163.com'
EMAIL_HOST_PASSWORD = 'wb18312801131wb'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = '[django] '