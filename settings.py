import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------------
# Only used locally. Render injects variables automatically.
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------
# SECRET KEY
# ---------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY environment variable not set")

# ---------------------------------------------------------------
# DEBUG MODE
# ---------------------------------------------------------------
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# ---------------------------------------------------------------
# ALLOWED HOSTS – FULLY RENDER COMPATIBLE
# ---------------------------------------------------------------
default_hosts = [
    'localhost',
    '127.0.0.1',
    'productauth-tpio.onrender.com',
    '.onrender.com', 
    'productauth-tpio.onrender.com (from RENDER_EXTERNAL_HOSTNAME)',
    '.onrender.com'
]

raw_env_hosts = os.environ.get("ALLOWED_HOSTS", "")
env_hosts = [h.strip() for h in raw_env_hosts.split(",") if h.strip()]

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    env_hosts.append(render_hostname)

env_hosts.append(".onrender.com")  # wildcard support

# ---------------------------------------------------------------
# ALLOWED HOSTS (Render-safe with normalization)
# ---------------------------------------------------------------

def normalize_host(host):
    """Remove trailing dot from host header."""
    return host.rstrip(".")

default_hosts = [
    normalize_host("localhost"),
    normalize_host("127.0.0.1"),
    normalize_host("productauth-tpio.onrender.com"),
    normalize_host(".onrender.com"),
]

raw_env_hosts = os.environ.get("ALLOWED_HOSTS", "")
env_hosts = [normalize_host(h.strip()) for h in raw_env_hosts.split(",") if h.strip()]

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    env_hosts.append(normalize_host(render_hostname))

# Final list
ALLOWED_HOSTS = default_hosts + env_hosts

# Remove duplicates and blanks
ALLOWED_HOSTS = list({h for h in ALLOWED_HOSTS if h})

print("🔥 ALLOWED_HOSTS:", ALLOWED_HOSTS)

# ---------------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------------
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "accounts",
    "blog",
    "authentication",
]

# ---------------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------
# URL CONFIG
# ---------------------------------------------------------------
ROOT_URLCONF = "productauth.urls"

# ---------------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ---------------------------------------------------------------
# WSGI
# ---------------------------------------------------------------
WSGI_APPLICATION = "productauth.wsgi.application"

# ---------------------------------------------------------------
# DATABASE (SQLite for now)
# ---------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_TZ = True

# ---------------------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------
# DEFAULT PRIMARY KEY
# ---------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
