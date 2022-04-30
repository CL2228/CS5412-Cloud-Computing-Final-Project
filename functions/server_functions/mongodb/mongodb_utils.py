"""
    mongoDB helper functions

    Author: Chenghui Li

    MongoDB's configurations:

    DB: cs5412-cl2228

    Collections:
    [tenant]:       tenants
    [guest]:        guests
    [unit]:         units
    [record]:       records
    [devices]:      devices
"""
import pymongo
from pymongo import MongoClient
from bson import ObjectId
from ..config import cosmosDBString, localMongoString, mongoDatabaseName
# from functions.server_functions.config import cosmosDBString, localMongoString, mongoDatabaseName
mongo_client = MongoClient(cosmosDBString)


############################################################################
# Insert Data Utilities
############################################################################
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


def check_duplicate(collection_name: str,
                    query_dict: dict,
                    database_name: str = mongoDatabaseName) -> bool:
    """
    check if there is existing data in the database
    :param collection_name: the collection name of the databse
    :param query_dict: query dictionary
    :param database_name: DEFAULT as cs5412
    :return: boolean, whether there is duplicate
    """
    try:
        database = mongo_client[database_name]
        collection_name = database[collection_name]
        if collection_name.find_one(query_dict) is not None:
            return True
        else:
            return False
    except Exception as ex:
        return True


def insert_with_dup_check(collection_name: str,
                          data: dict,
                          check_keys: list,
                          database_name: str = mongoDatabaseName):
    """
    insert data into database before duplicate check
    :param collection_name:
    :param data: a dictionary-format data to be inserted
    :param check_keys: a list of keys for checking duplicates, every key should be in data
    :param database_name:
    :return: [T / F , object_id / error_message]
    """
    if len(check_keys) == 0:
        return False, "You Must provide keys to check duplications"

    for key in check_keys:
        if key not in data.keys():
            return False, "Key [{}] is not in data".format(key)
        query_dict = {key: data[key]}
        if check_duplicate(collection_name, query_dict, database_name):
            return False, "Duplicate key-value: [{}]-[{}] detected".format(key, query_dict[key])

    state, message = insert(collection_name, data, database_name)
    return state, message


############################################################################
# Query Data Utilities
############################################################################
def query_one(collection_name: str,
              query_dict: dict,
              projections: dict = None,
              database_name: str = mongoDatabaseName):
    """
    query a piece of data from database
    :param projections:
    :param collection_name:
    :param query_dict:
    :param database_name:
    :return: [T / F, data / exception]
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        if "_id" in query_dict.keys() and type(query_dict['_id']) == str:
            query_dict['_id'] = ObjectId(query_dict['_id'])
        query_result = collection.find_one(query_dict, projections)
        if query_result is None:
            return False, "Data Not Found"
        return True, query_result
    except Exception as ex:
        return False, ex


def query_many(collection_name: str,
               query_dict: dict,
               projections: dict = None,
               sort_key=None,
               limit_num: int = 65536,
               database_name: str = mongoDatabaseName):
    """
        query_many function for mongoDB, this function can be used to query many pieces of data and limit the number,
        and sort the data by a key

        noted that currently in CosmosDB, if you want to sort the queried data by a key that other than "_id",
        you need to add indexing to this key, according to the documentation:
        https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb/mongodb-indexing#indexing-for-mongodb-server-version-36

    :param collection_name: the name of the collection in mongoDB
    :param query_dict: query conditions
    :param projections:
    :param sort_key: the key that used for sorting, if not provided, the queried data are not sorted by default
                    this parameter must be a str or a tuple
                    - str: specifies the key for soring
                    - tuple: must be in the format as (key, 1/-1)
                        1 for ascending order, -1 for descending order
    :param limit_num: limit the number of data that are returned, maximum as 65536
    :param database_name: the name of database, in this project, "cs5412-cl2228" is the default value
    :return: [T / F, data / message]
    """
    limit_num = min(65536, limit_num)
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        if "_id" in query_dict.keys() and type(query_dict['_id']) == str:
            query_dict['_id'] = ObjectId(query_dict['_id'])
        if sort_key is not None:
            if type(sort_key) == str:
                query_result = list(collection.find(query_dict, projections).sort(sort_key).limit(limit_num))
            elif type(sort_key) == tuple:
                assert len(sort_key) == 2 and type(sort_key[0]) == str and (sort_key[1] == -1 or sort_key[1] == 1),\
                    "wrong tuple format, the vliad format should be (key, 1/-1)"
                query_result = list(collection.find(query_dict, projections).sort(sort_key[0], sort_key[1]).limit(limit_num))
            else:
                raise ValueError("The 'sort_keys' parameter should be a string or a tuple")
        else:
            query_result = list(collection.find(query_dict, projections).limit(limit_num))
        # query_result = list(collection.find(query_dict))
        return len(query_result) > 0, query_result
    except Exception as ex:
        return False, ex


############################################################################
# Update Data Utilities
############################################################################
def update_one(collection_name: str,
               original_data: dict,
               update_data: dict,
               database_name: str = mongoDatabaseName):
    """
        update a piece of data in mongoDB
    :param collection_name: collection name
    :param original_data:   filter
    :param update_data:     updated data (K-V)
    :param database_name:
    :return: [T / F, message]
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        update_vals = {"$set": update_data}
        update_res = collection.update_one(original_data, update_vals)
        if not update_res.raw_result['updatedExisting']:
            return False, "Data doesn't exist or it is stale!"
        return True, "Updated successfully"
    except Exception as ex:
        return False, ex


############################################################################
# Update Data Utilities
############################################################################
def delete_one(collection_name: str,
               original_data: dict,
               database_name: str = mongoDatabaseName):
    """
    delete one piece of data based on filter
    :param collection_name: name of collection
    :param original_data:   filter, usually is the original data, for accuracy
    :param database_name:   [T / F, message]
    :return:
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        delete_res = collection.delete_one(original_data).raw_result['n'] > 0
        if delete_res:
            return True, "Deleted successfully"
        else:
            return False, "Data doesn't exist"
    except Exception as ex:
        return False, ex


def delete_many(collection_name: str,
                filter_dict: dict,
                database_name: str = mongoDatabaseName):
    pass


if __name__ == "__main__":
    data = {'timestamp': 1649651613.762,
                      'unit_id': '62475aaadd78bdc4e2448eb8',
                      'device_id': 'gates-hall-g01',
                      'blob_name': 'gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg',
                      'verified': False,
                      'verify_identity': 'Stranger',
                      'reference_img': None,
                      'confidence': 0.0}
    # print(insert("records", data))
    # print(query_many("records", {}, sort_dict={'timestamp': 1}))

    unit_data = {
        'building_name': "Phillips Hall",
        'address': '343 Campus Rd',
        'unit_number': '403',
        'tenants': {}
    }
    print(insert("units", unit_data))
