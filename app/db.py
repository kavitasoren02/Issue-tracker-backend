from __future__ import annotations
import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from functools import lru_cache

@lru_cache(maxsize=1)
def get_mongo_client() -> AsyncIOMotorClient:
    uri = os.getenv("MONGODB_URI", "mongodb+srv://kavitasoren2000_db_user:CZGioeHeTshWOdlp@cluster0.hb1eibt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return AsyncIOMotorClient(uri)

def get_db() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    db_name = os.getenv("MONGODB_DB", "issuetracker")
    return client[db_name]
