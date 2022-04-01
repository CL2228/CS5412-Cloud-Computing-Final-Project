from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
cosmosDBString = "mongodb://cs5412-final-project-cosmosdb:xszwNNn41aF2cMcJp7Xsd1R7W7bk3j4LdP94E1peFHGJba9DYPfQZMz9NEvxtnEkEHJ4oHHAeQbFRbYAjBVo0w==@cs5412-final-project-cosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cs5412-final-project-cosmosdb@"


# mongo_client = MongoClient("mongodb://127.0.0.1:27017/")


if __name__ == "__main__":
    mongo_client = MongoClient("mongodb://127.0.0.1:27017/")

    db = mongo_client["cs5412"]

    col = db["tenants"]

    data = col.find_one()
    data['first_name'] = "?"

    new_val = {"$set": {"first_name": "MZX", "last_name": "XXT"}}
    res = col.update_one(data, new_val)
    print(res.raw_result)
    data_2 = col.find_one()
    print(data_2)



