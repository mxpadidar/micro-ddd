from datetime import timedelta

from .env import Env

env = Env()

POSTGRES_URI = env.POSTGRES_URI

MINIO_ENDPOINT = env.MINIO_ENDPOINT
MINIO_ROOT_USER = env.MINIO_ROOT_USER
MINIO_ROOT_PASSWORD = env.MINIO_ROOT_PASSWORD

RABBITMQ_HOST = env.RABBITMQ_HOST
RABBITMQ_USER = env.RABBITMQ_DEFAULT_USER
RABBITMQ_PASS = env.RABBITMQ_DEFAULT_PASS

REDIS_HOST = env.REDIS_HOST
REDIS_PORT = env.REDIS_PORT
REDIS_DB = env.REDIS_DB

AUTH_SERVICE_URL = env.AUTH_SERVICE_URL

STORAGE_SERVICE_URL = env.STORAGE_SERVICE_URL

SECRET_KEY = "SecretKey"
ACCESS_TOKEN_LIFETIME = timedelta(seconds=60 * 60 * 24 * 7)
REFRESH_TOKEN_LIFETIME = timedelta(seconds=60 * 60 * 24 * 14)
JWT_ALGORITHM = "HS256"
