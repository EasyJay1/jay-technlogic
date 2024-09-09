from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

APPEND_SLASH = False


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's_8&hc^&p-k$ac(zwv#6c8n#hzg#)9d548wg)tcrg#16)deca!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ALLOWED_HOSTS = []


# Application definition


AUTH_USER_MODEL = "accounts.User"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

]

# Thired party apps
THIRED_PARTY_APPS = [
    "crispy_forms",
    "rest_framework",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.facebook",
]

# Custom apps
PROJECT_APPS = [
    "accounts.apps.AccountsConfig",
    "academy.apps.AcademyConfig",
    "result.apps.ResultConfig",
    "search.apps.SearchConfig",
    "quiz.apps.QuizConfig",
    "payments.apps.PaymentsConfig",
    "blogapp.apps.BlogappConfig",

]

# Combine all apps
INSTALLED_APPS = DJANGO_APPS + THIRED_PARTY_APPS + PROJECT_APPS


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': '427482717564-fvvcg5biief0olq6aff44n83n6bs71gi.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

SITE_ID = 1
import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blogapp.context_processors.appointments',  # Add this line
            ],
            'builtins': [],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# WSGI_APPLICATION = 'mysite.wsgi.app'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
     }
}

#DATABASES = {

 #   'default': {

  #      'ENGINE': 'django.db.backends.postgresql',
   #     'NAME': 'railway',
    #    'USER': 'postgres',
     #  'HOST': 'containers-us-west-178.railway.app',
      #  'PORT': '7344',

    #}

#}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_URL = '/media/'  # URL for serving media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Path to the media files directory

# settings.py
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'  # Redirect URL for anonymous users after email confirmation
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'contact'  # Redirect URL for authenticated users after email confirmation

#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = 'static/email_logs'

EMAIL_TIMEOUT = 15  # Timeout set to 15 seconds



# settings.py
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'jamesstarlit@gmail.com'  # Replace with your Gmail email address
EMAIL_HOST_PASSWORD = 'cymagbzckudvbpeb'  # Use your Gmail password or App Password


# settings.py
DEFAULT_FROM_EMAIL = 'noreply@easyjay.com'  # Replace with your sender email address
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[EASY-JAY TECHNOLOGY]'  # Replace with your desired email subject prefix
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True  # Set to False if you don't want to send email confirmation emails


