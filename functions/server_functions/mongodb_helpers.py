from pymongo import MongoClient
from bson import ObjectId
from .config import cosmosDBString

mongo_client = MongoClient(cosmosDBString)


def insert(database_name, collection_name, data):
    database = mongo_client[database_name]
    collection = database[collection_name]
    obj_id = collection.insert_one(data).inserted_id
    return obj_id
