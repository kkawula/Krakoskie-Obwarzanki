import os
from pymongo import MongoClient
from dotenv import load_dotenv


def init_db():

    load_dotenv()

    MONGO_URL = os.getenv("MONGO_URL")

    if not MONGO_URL:
        raise ValueError("You must set the MONGO_URL environment variable")

    client = MongoClient(MONGO_URL)
    database = client.get_database("pretzelShop")
    shops = database["shops"]
    
    users = database["users"]
    return shops, users
