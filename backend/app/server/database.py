import os

import certifi
import motor.motor_asyncio
from beanie import init_beanie
from server.models.shop import Shop
from server.models.user import User


async def init_db():
    MONGO_URL = os.getenv("MONGO_URL")

    if not MONGO_URL:
        raise ValueError("You must set the MONGO_URL environment variable")

    DB_NAME = os.getenv("DB_NAME")

    if not DB_NAME:
        raise ValueError("You must set the DB_NAME environment variable")

    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URL, tlsCAFile=certifi.where()
    )
    database = client.get_database(DB_NAME)

    # Create a 2d-sphere index on the 'location' field of the 'Shop' collection
    shop_collection = database.get_collection(Shop.Settings.name)
    await shop_collection.create_index([("location", "2dsphere")])

    await init_beanie(database=database, document_models=[Shop, User])
