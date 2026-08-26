from pymongo import MongoClient

from app.core.config import settings


client = MongoClient(settings.MONGODB_URL)

db = client[settings.MONGODB_DATABASE]

users_collection = db["users"]


def initialize_database():

    users_collection.create_index(
        "email",
        unique=True
    )


def get_database():
    return db


def get_users_collection():
    return users_collection