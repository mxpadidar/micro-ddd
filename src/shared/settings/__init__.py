from datetime import timedelta

from .env import Env

env = Env()

POSTGRES_URI = env.POSTGRES_URI

AUTH_SERVICE_URL = env.AUTH_SERVICE_URL

STORAGE_SERVICE_URL = env.STORAGE_SERVICE_URL

SECRET_KEY = "SecretKey"
ACCESS_TOKEN_LIFETIME = timedelta(seconds=60 * 60 * 24 * 7)
REFRESH_TOKEN_LIFETIME = timedelta(seconds=60 * 60 * 24 * 14)
JWT_ALGORITHM = "HS256"
