#file: project/settings.py
# A settings modul felelős a Django projekt konfigurációjáért.
# Betöltjük a .env értékeit, beállítjuk a magyar nyelvet, és konfiguráljuk
# a static, media és template útvonalakat.


from pathlib import Path
from dotenv import load_dotenv
import os


# -------------------------------------------------------------------------
# .env fájl betöltése
# -------------------------------------------------------------------------
load_dotenv()


# -------------------------------------------------------------------------
# Alap könyvtár meghatározása
# -------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------------------------------------------------------------
# Biztonsági beállítások
# -------------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "ccais.default-dev-key")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")


# -------------------------------------------------------------------------
# Alkalmazások regisztrációja
# -------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Alkalmazások
    'core.apps.CoreConfig',
]


# -------------------------------------------------------------------------
# Middleware komponensek
# -------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -------------------------------------------------------------------------
# Fő URL konfiguráció
# -------------------------------------------------------------------------
ROOT_URLCONF = 'project.urls'


# -------------------------------------------------------------------------
# Template rendszer konfiguráció
# -------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Projekt szintű sablonok helye
        'DIRS': [BASE_DIR / "templates"],

        # App szintű templates könyvtárak engedélyezése
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -------------------------------------------------------------------------
# WSGI alkalmazás
# -------------------------------------------------------------------------
WSGI_APPLICATION = 'project.wsgi.application'


# -------------------------------------------------------------------------
# Adatbázis – SQLite fejlesztési módhoz
# -------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# -------------------------------------------------------------------------
# Jelszó validáció
# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
# Lokalizáció – magyar beállítások
# -------------------------------------------------------------------------
LANGUAGE_CODE = 'hu-hu'
TIME_ZONE = 'Europe/Budapest'
USE_I18N = True
USE_TZ = True


# -------------------------------------------------------------------------
# Statikus fájlok beállítása
# -------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"


# -------------------------------------------------------------------------
# Media fájlok beállítása (feltöltött asset-ek)
# -------------------------------------------------------------------------
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"


# -------------------------------------------------------------------------
# Django modell alapértelmezett elsődleges kulcstípus
# -------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------------------------------------------------------------------
# AI szolgáltatások konfigurációi az .env-ből
# Ezeket később service modulok fogják használni.
# -------------------------------------------------------------------------

PLUTOAI_SETTINGS = {
    "api_key": os.getenv("PLUTOAI_API_KEY"),
    "base_url": os.getenv("PLUTOAI_BASE_URL"),
    "model": os.getenv("PLUTOAI_MODEL"),
    "verify_ssl": os.getenv("PLUTOAI_VERIFY_SSL", "False") == "True",
}

OPENAI_SETTINGS = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL"),
}

PERPLEXITY_SETTINGS = {
    "api_key": os.getenv("PER_API_KEY"),
    "base_url": os.getenv("PER_BASE_URL"),
}
