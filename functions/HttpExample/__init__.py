import logging

import azure.functions as func

from ..server_functions.blob import azure_blob_helpers
import datetime
import pickle
import json
# from ..server_functions.eventhub import eventhub_utils


def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage], eventHubOutput: func.Out[bytes]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    time_now = datetime.datetime.now()

    # eventHubOutput
    event_body = {'device_id': "gates-hall-g01",
                  'blob_name': "gates-hall-g01/records/b2be69f0-c3ff-4801-9fad-ef2eec87e52b.jpg",
                  'unit_id': "62475aaadd78bdc4e2448eb8"}
    
    # eventHubOutput.set(pickle.dumps(event_body))
    msg.set("Function trigger at {}".format(time_now.time()))

    res_body = [
        {
        "name": "MZXCNMCNm"
        }
    ]

    res_headers = { 'Content-Type': 'application/json' }


    response = func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)
    return response
