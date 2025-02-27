from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = "stm_mongo_db"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

async def get_collection(collection_name: str):
    return db[collection_name]
