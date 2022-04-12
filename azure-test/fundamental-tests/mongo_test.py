import datetime
import pprint
from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
cosmosDBString = "mongodb://cs5412-final-project-cosmosdb:7NTur9WLYF1d61UlU16shuaEDi2WJwBI78tvwhpVidrqXl83p2qBSchBAOVE1jYKCkgTNiHoe9hHHuhaLHxKvw==@cs5412-final-project-cosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@cs5412-final-project-cosmosdb@"
localDBString = "mongodb://127.0.0.1:27017/"
mongoDatabaseName = "cs5412-cl2228"

mongo_client = MongoClient(cosmosDBString)


def insert(collection_name: str,
           data: dict,
           database_name: str = mongoDatabaseName):
    """
    insert a piece of data to database, without duplicate check
    :param collection_name: collection name of mongoDB
    :param data: data, which should be an object?
    :param database_name: database name, default as in config
    :return:
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        obj_id = collection.insert_one(data).inserted_id
        return True, obj_id
    except Exception as ex:
        return False, ex


def query_many(collection_name: str,
               query_dict: dict,
               sort_key=None,
               limit_num: int = 65536,
               database_name: str = mongoDatabaseName):
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        if "_id" in query_dict.keys() and type(query_dict['_id']) == str:
            query_dict['_id'] = ObjectId(query_dict['_id'])
        if sort_key is not None:
            if type(sort_key) == str:
                query_result = list(collection.find(query_dict).sort(sort_key).limit(limit_num))
            elif type(sort_key) == tuple:
                assert len(sort_key) == 2 and type(sort_key[0]) == str and (sort_key[1] == -1 or sort_key[1] == 1),\
                    "wrong tuple format, the vliad format should be (key, 1/-1)"
                query_result = list(collection.find(query_dict).sort(sort_key[0], sort_key[1]).limit(limit_num))
            else:
                raise ValueError("The 'sort_keys' parameter should be a string or a tuple")
        else:
            query_result = list(collection.find(query_dict).limit(limit_num))
        # query_result = list(collection.find(query_dict))
        return len(query_result) > 0, query_result
    except Exception as ex:
        return False, ex


def custom_comparator_generator(key, direction):
    def custom_cmp(a):
        return a * 2
    return custom_cmp

if __name__ == "__main__":
    data = {
        'timestamp': datetime.datetime.now().timestamp(),
        'unit_id': "62475aaadd78bdc4e2448eb8",
        'face_img': "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
        'device_id': "gates-hell-g01",
        'ref_img': None,
        'verified': False,
        'verify_identity': "Stranger"
    }
    query_status, query_data = query_many("records", {}, sort_key=("_id", -1))
    print(query_status)
    pprint(query_data)
    func = custom_comparator_generator("", "")
    print(func(323))
    t1 = (1, "erewr", 3)
    print(type(t1[1]))

