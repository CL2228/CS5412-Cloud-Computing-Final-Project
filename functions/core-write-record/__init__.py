import datetime
from typing import List
import logging
import azure.functions as func
import pickle
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def main(events: List[func.EventHubEvent],
         outputQueueItem: func.Out[func.QueueMessage]):
    for event in events:
        event_body = pickle.loads(event.get_body())
        logging.info('Python EventHub trigger processed an event: %s',
                     event_body)
        res = handle_one_event(event)
        outputQueueItem.set("Handle one core-write-record event at {}, result:{}".format(datetime.datetime.now(),
                                                                                         event_body['verified']))


def handle_one_event(event: func.EventHubEvent):
    record_data = {
        'timestamp': 0.0,
        'unit_id': "",
        'face_img': "",
        'device_id': "",
        'ref_img': None,
        'verified': False,
        'verify_identity': "Stranger"
    }
    try:
        event_body = pickle.loads(event.get_body())
        record_data['timestamp'] = event_body['timestamp']
        record_data['unit_id'] = event_body['unit_id']
        record_data['face_img'] = event_body['blob_name']
        record_data['device_id'] = event_body['device_id']
        record_data['ref_img'] = event_body['reference_img']
        record_data['verified'] = event_body['verified']
        record_data['verify_identity'] = event_body['verify_identity']
        CHECK_FUNCTIONS['record'](record_data)
        mongodb_utils.insert("records", record_data)
        return "success"
    except Exception as ex:
        return str(ex)

