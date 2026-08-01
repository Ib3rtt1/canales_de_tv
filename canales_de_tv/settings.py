"""
Django settings for canales_de_tv project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga variables desde un archivo .env en la raíz del proyecto (no se
# versiona, ver .env.example para la lista de variables esperadas).
# Si no existe .env (p. ej. en producción, donde las variables ya están
# en el entorno del proceso), load_dotenv() simplemente no hace nada.
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in (
        "1", "true", "yes", "on",
    )


def env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ======================================================
# SEGURIDAD
# ======================================================

# Antes: SECRET_KEY hardcodeada en el repo y DEBUG=True fijo -> cualquiera
# con el código tenía la clave de firma de sesiones/CSRF, y un despliegue
# a producción heredaba DEBUG=True (páginas de error con stack trace y
# variables de entorno visibles) a menos que alguien lo recordara cambiar
# a mano en cada lugar. Ahora todo sale de variables de entorno.

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = env_bool("DJANGO_DEBUG", default=False)

if not SECRET_KEY:
    if DEBUG:
        # Solo para desarrollo local sin .env configurado. Nunca usar
        # esta clave en producción (DEBUG=False la rechaza más abajo).
        SECRET_KEY = "django-insecure-desarrollo-local-no-usar-en-produccion"
    else:
        raise RuntimeError(
            "DJANGO_SECRET_KEY no está definida. Configúrala en tu .env "
            "o en las variables de entorno del servidor (ver .env.example)."
        )

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")

# Necesario en Django 4+ para aceptar POST (login, dashboard, etc.)
# detrás de un proxy/CDN como Render, con esquema https:// incluido.
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

if not DEBUG:
    # Render (y proveedores similares) terminan TLS en su proxy y
    # reenvían por HTTP interno; sin esto, request.is_secure() siempre
    # da False y SECURE_SSL_REDIRECT provoca un loop de redirects.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7  # 1 semana; subir tras confirmar que todo sirve por HTTPS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    X_FRAME_OPTIONS = "DENY"


# ======================================================
# APLICACIONES
# ======================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto
    "guia_tv",
    "accounts",
]


# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise sirve los archivos de STATIC_ROOT directamente desde
    # la app en producción (Render no sirve estáticos por sí solo).
    # Va inmediatamente después de SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "canales_de_tv.urls"


# ======================================================
# TEMPLATES
# ======================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "canales_de_tv.wsgi.application"


# ======================================================
# BASE DE DATOS
# ======================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ======================================================
# VALIDACIÓN DE CONTRASEÑAS
# ======================================================

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


# ======================================================
# INTERNACIONALIZACIÓN
# ======================================================

LANGUAGE_CODE = "es-cl"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_TZ = True


# ======================================================
# ARCHIVOS ESTÁTICOS
# ======================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Storage moderno de Django 5 para estáticos: WhiteNoise + hash de
# nombre de archivo (cache-busting) + compresión gzip/br automática.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ======================================================
# ARCHIVOS MULTIMEDIA
# ======================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ======================================================
# AUTO FIELD
# ======================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
