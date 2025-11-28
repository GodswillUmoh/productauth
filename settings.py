import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES (LOCAL ONLY)
# ---------------------------------------------------------------
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
# ALLOWED HOSTS — CLEAN, CORRECT, 100% WORKING ON RENDER
# ---------------------------------------------------------------
def normalize(hostname: str):
    """Remove spaces and trailing dots."""
    return hostname.strip().rstrip(".")

# ---------------------------------------------------------------
# ALLOWED HOSTS — FINAL FIX
# ---------------------------------------------------------------
print("Incoming Render host:", os.environ.get("RENDER_EXTERNAL_HOSTNAME"))

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "productauth-tpio.onrender.com",  # your site
    ".onrender.com",                  # wildcard (subdomains)
]

# Add Render auto hostname — usually same as your URL
render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host.strip())

# Add user-defined env values if any
extra_hosts = os.environ.get("ALLOWED_HOSTS")
if extra_hosts:
    ALLOWED_HOSTS.extend([h.strip() for h in extra_hosts.split(",") if h.strip()])

# Remove duplicates
ALLOWED_HOSTS = list(set(ALLOWED_HOSTS))

print("🔥 FINAL ALLOWED_HOSTS:", ALLOWED_HOSTS)

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
# DATABASE
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
