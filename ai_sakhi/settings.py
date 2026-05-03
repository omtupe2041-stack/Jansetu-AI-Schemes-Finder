from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DJANGO_DEBUG', 'false').lower() in {'1', 'true', 'yes'}
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY', 'django-insecure-aisakhi-dev-only')

allowed_hosts = {
    'localhost',
    '127.0.0.1',
    'testserver',
    '.vercel.app',
    '.onrender.com',
}

vercel_url = os.environ.get('VERCEL_URL')
if vercel_url:
    allowed_hosts.add(vercel_url)

render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname:
    allowed_hosts.add(render_hostname)

allowed_hosts.update(
    host.strip()
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
    if host.strip()
)

ALLOWED_HOSTS = sorted(allowed_hosts)

csrf_trusted_origins = {
    'http://localhost',
    'http://127.0.0.1',
    'http://testserver',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://*.vercel.app',
    'https://*.onrender.com',
}
if vercel_url:
    csrf_trusted_origins.add(f'https://{vercel_url}')
if render_hostname:
    csrf_trusted_origins.add(f'https://{render_hostname}')

CSRF_TRUSTED_ORIGINS = sorted(csrf_trusted_origins)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'women_app',
]

try:
    import whitenoise  # noqa: F401
except ImportError:  # pragma: no cover - local fallback when deps are not installed yet
    whitenoise = None

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if whitenoise is not None:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'ai_sakhi.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'women_app' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

WSGI_APPLICATION = 'ai_sakhi.wsgi.application'

try:
    import dj_database_url
except ImportError:  # pragma: no cover - local fallback when deps are not installed yet
    dj_database_url = None

if dj_database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'women_app' / 'static']
STATIC_ROOT = BASE_DIR / 'public' / 'staticfiles'
if whitenoise is not None:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
