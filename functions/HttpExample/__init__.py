import logging

import azure.functions as func

from ..server_functions.blob import azure_blob_helpers


def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    msg.set("LCH Messge")
    response = func.HttpResponse("message", status_code=200)
    return response
