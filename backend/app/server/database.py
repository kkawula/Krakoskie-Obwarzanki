import os

import motor.motor_asyncio
from beanie import init_beanie
from dotenv import load_dotenv
from server.models.shop import Shop


async def init():
    load_dotenv()

    MONGO_URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("DB_NAME")

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    database = client.get_database(DB_NAME)

    # Create a 2dsphere index on the 'location' field of the 'Shop' collection
    shop_collection = database.get_collection("Shop")
    await shop_collection.create_index([("location", "2dsphere")])

    await init_beanie(database=database, document_models=[Shop])
