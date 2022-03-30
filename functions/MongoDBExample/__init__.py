import logging

import azure.functions as func
from ..server_functions import mongodb_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    obj_id = mongodb_helpers.insert("test", "people", {"message": "hello"})

    return func.HttpResponse(str(obj_id))
