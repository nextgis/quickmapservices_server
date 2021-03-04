"""
Django settings for qms_site project.
"""
import os

# Override
DEBUG = os.getenv("IS_DEBUG", 'true').lower() in ['true', '1']
if DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOST','')]

DATABASE_NAME = os.getenv('DATABASE_NAME','')
DATABASE_USER = os.getenv('DATABASE_USER','')
DATABASE_PASS = os.getenv('DATABASE_PASS','')
DATABASE_HOST = os.getenv('DATABASE_HOST','')
DATABASE_PORT = os.getenv('DATABASE_PORT','')


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,	                # SET THIS!
        'PASSWORD': DATABASE_PASS,             # SET THIS!
        'HOST': DATABASE_HOST,                 # SET THIS!
        'PORT': DATABASE_PORT
    }
}

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Secure
SECRET_KEY = 'ASDFLKAL;SKDF;LKN3M,N2LKJ34H5KJF;GHSUI898993243(N	KLS-FQ9'
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# NGID Auth
NGID_CLIENT_ID = 'jQBKtVVaEWTIZT9yZQt9pet6168iTD5sR27dYXT8'
NGID_CLIENT_SECRET = 'AlWUFBZXWT0a7wzuFt1rvajgVDuyQXwIOvEWPRVjAJm1Wcx9b0vPTYCPgPfaaqpEGGmZNK9MKNQpfl9n1V2VUwaAG8XrFAybxpCDz1r8m5wvfnQZZdxBZ3aHhmZkVw77'



# reCaptcha settings
RECAPTCHA_PUBLIC_KEY = '6Lcu7xUUAAAAAJ-fUPBp50JiHqkSJHeqLCf0uFxp'
RECAPTCHA_PRIVATE_KEY = '6Lcu7xUUAAAAALwAK5Mlc6ioggDVvjccO4HeFR2j'
NOCAPTCHA = True


# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''                     # SET THIS!
EMAIL_PORT = 587                    # SET THIS!
EMAIL_HOST_USER = ''                # SET THIS!
EMAIL_HOST_PASSWORD = ''            # SET THIS!
EMAIL_USE_TLS = True                # SET THIS!
EMAIL_USE_SSL = False               # SET THIS!
DEFAULT_FROM_EMAIL = ''             # SET THIS!

# Checker settings
SERVICE_CHECK_TIMEOUT = 10  # secs
