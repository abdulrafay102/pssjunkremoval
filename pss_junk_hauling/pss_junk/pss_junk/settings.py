from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-change-this-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pss_junk.urls'

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === YOUR SETTINGS ===
ANTHROPIC_API_KEY = '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'

BUSINESS_NAME = "PSS Junk Hauling"
BUSINESS_PHONE = "(216-300-8126)"
BUSINESS_AREA = "Cleveland, Ohio"
BUSINESS_HOURS = "Monday–Saturday, 7am–7pm"
SERVICE_AREAS = [
    "Cleveland", "Cleveland Heights", "Parma", "Lakewood",
    "Euclid", "Strongsville", "Mentor", "Westlake",
    "North Olmsted", "Brook Park", "Garfield Heights"
]
