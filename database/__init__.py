from tortoise import Tortoise
from settings import TORTOISE_PSQL_CONFIG


async def init_connection():
    await Tortoise.init(config=TORTOISE_PSQL_CONFIG)


async def generate_schemas():
    await Tortoise.generate_schemas(safe=True)

