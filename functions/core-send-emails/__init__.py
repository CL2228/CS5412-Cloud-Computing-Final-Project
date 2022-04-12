import datetime
from typing import List
import logging

import azure.functions as func
import pickle
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.email import email_highlevel_helper


def main(events: List[func.EventHubEvent],
         outputQueueItem: func.Out[func.QueueMessage]):
    for event in events:
        event_body = pickle.loads(event.get_body())
        logging.info('Python EventHub trigger processed an event: %s',
                     event_body)
        handle_res = handle_one_event(event, outputQueueItem)
        print(handle_res)


def handle_one_event(event: func.EventHubEvent,
                     outputQueueItem: func.Out[func.QueueMessage]):
    try:
        event_body = pickle.loads(event.get_body())

        unit_existed, unit_data = mongodb_utils.query_one("units", {'_id': event_body['unit_id']})
        if not unit_existed:
            return False, "Unit does not exist"
        logging.info("tenant list:{}".format(unit_data['tenants']))

        for tenant_email in unit_data['tenants'].keys():
            email_highlevel_helper.send_warning_email(tenant_email, unit_data, event_body['timestamp'])
        outputQueueItem.set("Successfully called at {}, with unit_id:{}".format(datetime.datetime.now(), event_body['unit_id']))
        return True, "success"
    except Exception as ex:
        outputQueueItem.set("Error occurred at {}, with exception:{}".format(datetime.datetime.now(), str(ex)))
        return False, str(ex)
