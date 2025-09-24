from __future__ import annotations
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache

@lru_cache(maxsize=1)
def get_mongo_client() -> AsyncIOMotorClient:
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    return AsyncIOMotorClient(uri)

def get_db() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    db_name = os.getenv("MONGODB_DB", "issuetracker")
    return client[db_name]
