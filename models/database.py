from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set.")
else:
    print(f"Connecting to MongoDB at {MONGO_URL}")

# Initialize the MongoDB client (SYNC, not ASYNC)
client = MongoClient(MONGO_URL)
DATABASE_NAME = "stm_mongo_db"
db = client[DATABASE_NAME]

def check_connection():
    """Checks if the database connection is active (Synchronous)."""
    try:
        result = db.command("ping")
        print("✅ MongoDB Connection Successful:", result)
        return True
    except Exception as e:
        raise ConnectionError(f"❌ Failed to connect to MongoDB: {e}")

# Call check_connection right after connecting
if check_connection():
    print("Connected to MongoDB successfully.")
else:
    raise ConnectionError("Failed to connect to MongoDB.")

def get_collection(collection_name: str):
    """Returns a MongoDB collection."""
    return db[collection_name]
