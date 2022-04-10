import logging
import json
import azure.functions as func
import datetime
# from ..server_functions.mongodb import mongodb_utils
# from ..server_functions.jwt.jwt_utils import generate_jwt

if __name__ == "__main__":
    t1 = datetime.datetime.fromtimestamp(1649547831)
    t2 = datetime.datetime.fromtimestamp(1649547232)
    print(t1.time())
    print(t2.time())
    print(t2 < t1)




















