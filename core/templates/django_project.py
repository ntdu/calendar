# -*- coding: utf-8 -*-
import os
from typing import Dict

from .settings import DjangoSetting


def create_django_setting(env: DjangoSetting, **kwargs) -> Dict:
    ROOT_DIR = os.getcwd()
    # sop_chat_service/
    APPS_DIR = os.path.join(os.getcwd(), 'src')
    print('root_dir', ROOT_DIR)
    print('app_dir', APPS_DIR)
    ADMINS = [("""SCC""", "scc@example.com")]

    dj_settings = {
        'DEBUG': env.DJANGO_DEBUG,
        'SECRET_KEY': env.DJANGO_SECRET_KEY,

        'DATABASES': env.create_django_databases(),

        'ALLOWED_HOSTS': env.DJANGO_ALLOWED_HOSTS,

        # CORS
        'CORS_ALLOWED_ORIGINS': env.DJANGO_CORS_ALLOWED_ORIGINS,
        'CORS_ALLOW_METHODS': env.DJANGO_CORS_ALLOWED_METHOD,


        'USE_TZ' : env.DJANGO_USE_TZ,
        'TIME_ZONE': env.DJANGO_TIMEZONE,
        # https://docs.djangoproject.com/en/dev/ref/settings/#language-code
        'LANGUAGE_CODE' : "en-us",
        # https://docs.djangoproject.com/en/dev/ref/settings/#site-id
        'SITE_ID' : 1,
        # https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
        'USE_I18N' : True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
        'USE_L10N' : True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
        'LOCALE_PATHS': [os.path.join(ROOT_DIR, 'locale')],

        # https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
        'DEFAULT_AUTO_FIELD' : "django.db.models.BigAutoField",

        # APPS
        # ------------------------------------------------------------------------------
        'INSTALLED_APPS' : [
            # DJANGO_APPS-----------------
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django.contrib.humanize",  # Handy template tags
            "django.contrib.admin",
            "django.forms",
            # "channels",

            # THIRD_PARTY_APPS-----------   # NOSONAR
            # "crispy_forms",
            # "crispy_bootstrap5",
            "allauth",
            "allauth.account",
            "allauth.socialaccount",
            "django_celery_beat",
            "rest_framework",
            "rest_framework.authtoken",
            "corsheaders",
            # "drf_spectacular",
            'storages',     # s3 boto3
            'django_celery_results',
            'django.contrib.postgres',
        ],

        # AUTHENTICATION
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
        'AUTHENTICATION_BACKENDS': [
            "django.contrib.auth.backends.ModelBackend",
            "allauth.account.auth_backends.AuthenticationBackend",
        ],
        # https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
        'AUTH_USER_MODEL': "users.User",
        # https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
        'LOGIN_REDIRECT_URL': "users:redirect",
        # https://docs.djangoproject.com/en/dev/ref/settings/#login-url
        'LOGIN_URL': "account_login",

        # PASSWORDS
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
        'PASSWORD_HASHERS': [
            # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
            "django.contrib.auth.hashers.Argon2PasswordHasher",
            "django.contrib.auth.hashers.PBKDF2PasswordHasher",
            "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
            "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        ],
        # https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
        'AUTH_PASSWORD_VALIDATORS': [
            {
                "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
            },
            {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
            {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
            {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
        ],



        # MIDDLEWARE
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#middleware
        'MIDDLEWARE': [
            "django.middleware.security.SecurityMiddleware",
            "corsheaders.middleware.CorsMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.locale.LocaleMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.common.BrokenLinkEmailsMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],

        # STATIC
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#static-root
        'STATIC_ROOT': os.path.join(ROOT_DIR, 'staticfiles'),
        # https://docs.djangoproject.com/en/dev/ref/settings/#static-url
        'STATIC_URL': env.DJANGO_STATIC_URL,
        # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
        'STATICFILES_DIRS': [os.path.join(ROOT_DIR, 'static')],
        # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
        'STATICFILES_FINDERS': [
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ],
        'STATICFILES_STORAGE': "whitenoise.storage.CompressedManifestStaticFilesStorage",

        # MEDIA
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#media-root
        'MEDIA_ROOT': os.path.join(APPS_DIR, 'media'),
        # https://docs.djangoproject.com/en/dev/ref/settings/#media-url
        'MEDIA_URL': env.DJANGO_MEDIA_URL,

        # TEMPLATES
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#templates
        'TEMPLATES': [
            {
                # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
                "DIRS": [os.path.join(APPS_DIR, "templates")],
                # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
                "APP_DIRS": True,
                "OPTIONS": {
                    # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.static",
                        "django.template.context_processors.tz",
                        "django.contrib.messages.context_processors.messages",
                        "src.users.context_processors.allauth_settings",
                    ],
                },
            }
        ],

        # django rest framework
        'REST_FRAMEWORK': {
            "DEFAULT_AUTHENTICATION_CLASSES": (
                "rest_framework.authentication.SessionAuthentication",
                "rest_framework.authentication.TokenAuthentication",
            ),
            "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
            "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        },


        # https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
        'FORM_RENDERER': "django.forms.renderers.TemplatesSetting",

        # http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
        'CRISPY_TEMPLATE_PACK': "bootstrap5",
        'CRISPY_ALLOWED_TEMPLATE_PACKS': "bootstrap5",

        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
        'FIXTURE_DIRS': os.path.join(APPS_DIR, 'fixtures'),

        # SECURITY
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
        'SESSION_COOKIE_HTTPONLY': True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
        'CSRF_COOKIE_HTTPONLY': True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
        'SECURE_BROWSER_XSS_FILTER': True,
        # https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
        'X_FRAME_OPTIONS': "DENY",

        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
        'SECURE_PROXY_SSL_HEADER': env.DJANGO_SECURE_PROXY_SSL_HEADER,
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
        'SECURE_SSL_REDIRECT': env.DJANGO_SECURE_SSL_REDIRECT,
        # https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
        'SESSION_COOKIE_SECURE': env.DJANGO_SESSION_COOKIE_SECURE,
        # https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
        'CSRF_COOKIE_SECURE': env.DJANGO_CSRF_COOKIE_SECURE,
        # https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
        # -> set this to 60 seconds first and then to 518400 once you prove the former works
        'SECURE_HSTS_SECONDS': env.DJANGO_SECURE_HSTS_SECONDS,
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
        'SECURE_HSTS_INCLUDE_SUBDOMAINS': env.DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS,
        # https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
        'SECURE_HSTS_PRELOAD': env.DJANGO_SECURE_HSTS_PRELOAD,
        # https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
        'SECURE_CONTENT_TYPE_NOSNIFF': env.DJANGO_SECURE_CONTENT_TYPE_NOSNIFF,


        # EMAIL
        # ------------------------------------------------------------------------------
        # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
        'EMAIL_BACKEND': env.DJANGO_EMAIL_BACKEND,
        # https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
        'EMAIL_TIMEOUT': 5,


        # ADMIN
        # ------------------------------------------------------------------------------
        # Django Admin URL.
        'ADMIN_URL': env.DJANGO_ADMIN_URL,
        # https://docs.djangoproject.com/en/dev/ref/settings/#admins
        'ADMINS': ADMINS,
        # https://docs.djangoproject.com/en/dev/ref/settings/#managers
        'MANAGERS': ADMINS,


        # django-allauth
        # ------------------------------------------------------------------------------
        'ACCOUNT_ALLOW_REGISTRATION': env.DJANGO_ACCOUNT_ALLOW_REGISTRATION,
        # https://django-allauth.readthedocs.io/en/latest/configuration.html
        'ACCOUNT_AUTHENTICATION_METHOD': env.DJANGO_ACCOUNT_AUTHENTICATION_METHOD,
        # https://django-allauth.readthedocs.io/en/latest/configuration.html
        'ACCOUNT_EMAIL_REQUIRED': True,
        # https://django-allauth.readthedocs.io/en/latest/configuration.html
        'ACCOUNT_EMAIL_VERIFICATION': "mandatory",
        # https://django-allauth.readthedocs.io/en/latest/configuration.html
        'ACCOUNT_ADAPTER': "src.users.adapters.AccountAdapter",
        # https://django-allauth.readthedocs.io/en/latest/forms.html
        'ACCOUNT_FORMS': {"signup": "src.users.forms.UserSignupForm"},
        # https://django-allauth.readthedocs.io/en/latest/configuration.html
        'SOCIALACCOUNT_ADAPTER': "src.users.adapters.SocialAccountAdapter",
        # https://django-allauth.readthedocs.io/en/latest/forms.html
        'SOCIALACCOUNT_FORMS': {"signup": "src.users.forms.UserSocialSignupForm"},


        # django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
        'CORS_URLS_REGEX': r"^/api/.*$",

        'LOGGING': {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
            "formatters": {
                "verbose": {
                    "format": "%(levelname)s %(asctime)s %(module)s "
                    "%(process)d %(thread)d %(message)s"
                }
            },
            "handlers": {
                "mail_admins": {
                    "level": "ERROR",
                    "filters": ["require_debug_false"],
                    "class": "django.utils.log.AdminEmailHandler",
                },
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "verbose",
                },
                'celery': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'celery.log',
                    'formatter': 'simple',
                    'maxBytes': 1024 * 1024 * 100,  # 100 mb
                },
            },
            "root": {"level": "INFO", "handlers": ["console"]},
            "loggers": {
                "django.request": {
                    "handlers": ["mail_admins"],
                    "level": "ERROR",
                    "propagate": True,
                },
                "django.security.DisallowedHost": {
                    "level": "ERROR",
                    "handlers": ["console", "mail_admins"],
                    "propagate": True,
                },
                'celery': {
                    'handlers': ['celery', 'console'],
                    'level': 'DEBUG',
                },
            },
        },

        'DEFAULT_FILE_STORAGE': "storages.backends.s3boto3.S3Boto3Storage",
        'AWS_ACCESS_KEY_ID': "Bn6aG5NeEcpSCCAx",
        'AWS_SECRET_ACCESS_KEY': "bfHx6nlrqrddWH5uT4axHJ3HCMZ1e1Zg",
        'AWS_STORAGE_BUCKET_NAME': "sop-dev",
        'AWS_DEFAULT_ACL': None,
        'AWS_QUERYSTRING_AUTH': True,
        'AWS_S3_FILE_OVERWRITE': False,


        'AWS_S3_ENDPOINT_URL': "http://172.24.222.114:9000",

    }

    # your configuration here
    # or update after get return instance
    if kwargs:
        dj_settings.update(kwargs)

    return dj_settings
