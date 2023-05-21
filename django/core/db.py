# To use Neon with Django, you have to create a Project on Neon and specify the project connection settings in your settings.py in the same way as for standalone Postgres.
'''

from core.env import config
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL= config("DATABASE_URL", default=None)
if DATABASE_URL is not None:
    DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}
'''
from core.env import config
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL_MAIN = config("DATABASE_URL_MAIN", default=None)
DATABASE_URL_DEV = config("DATABASE_URL_DEV", default=None)

if DATABASE_URL_MAIN is not None:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL_MAIN,
            conn_max_age=600,
            conn_health_checks=True
        )
    }
elif DATABASE_URL_DEV is not None:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL_DEV,
            conn_max_age=600,
            conn_health_checks=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
