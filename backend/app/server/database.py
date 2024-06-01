import os
import motor.motor_asyncio
from dotenv import load_dotenv
from beanie import init_beanie
from server.models.shop import Shop


async def init_db():
    load_dotenv()

    MONGO_URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("DB_NAME")

    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    database = client.get_database(DB_NAME)

    await init_beanie(database=database, document_models=[Shop])
