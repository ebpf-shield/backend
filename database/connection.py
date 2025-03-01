from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI")
db_client = None

async def connect_to_mongo():
    global db_client
    db_client = AsyncIOMotorClient(MONGO_URI)
    print("Connected to MongoDB")

async def close_mongo_connection():
    global db_client
    if db_client:
        db_client.close()
        print("Closed MongoDB connection")
