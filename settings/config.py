from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
POSTGRES_USER = env.str("POSTGRES_USER", default="aiogram")
POSTGRES_DB = env.str("POSTGRES_DB", default="aiogram")
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

TORTOISE_PSQL_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': POSTGRES_HOST,
                'port': POSTGRES_PORT,
                'user': POSTGRES_USER,
                'password': POSTGRES_PASSWORD,
                'database': POSTGRES_DB,
            }
        },
        'default': POSTGRES_URI,
    },
    'apps': {
        'aerich': {
            'models': ['aerich.models'],
        },
        'users': {
            'models': ['apps.users.repository.orm_models'],
            'default_connection': 'default',
        },
        'schedule': {
            'models': ['apps.schedule.repository.orm_models'],
            'default_connection': 'default',
        },
    },
    'use_tz': True,
    'timezone': 'Europe/Moscow'
}

