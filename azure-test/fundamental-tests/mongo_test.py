from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint

cosmosDBString = "mongodb://cs5412-final-project-cosmosdb:xszwNNn41aF2cMcJp7Xsd1R7W7bk3j4LdP94E1peFHGJba9DYPfQZMz9NEvxtnEkEHJ4oHHAeQbFRbYAjBVo0w==@cs5412-final-project-cosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cs5412-final-project-cosmosdb@"


# mongo_client = MongoClient("mongodb://127.0.0.1:27017/")


if __name__ == "__main__":
    mongo_client = MongoClient(cosmosDBString)

    db = mongo_client["test"]

    col = db["people"]


    for i in range(10):
        customer = {
            "email": "cl2228@cornell.edu",
            "password": "cl2228",
            "name": "Chenghui Li"
        }
        print(col.insert_one(customer).inserted_id)

    # query = {"email": "cl2228@cornell.edu"}
    # li = ["abc", "erew", "erw"]
    # new_vals = {"$set": {'name': li}}
    # res = col.update_many(query, new_vals)
    # print(res.raw_result)
    ult = col.find_one({"_id": ObjectId("6243c235561c9ad19f9c58b9")})
    # print(result)
    # res

