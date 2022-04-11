import datetime
from typing import List
import logging
import azure.functions as func
import pickle
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt import jwt_utils


def main(events: List[func.EventHubEvent],
         outputQueueItem: func.Out[func.QueueMessage]):
    for event in events:
        logging.info('Python EventHub trigger processed an event: %s',
                        pickle.loads(event.get_body()))
        handle_one_event(event)
    outputQueueItem.set("Garbage collection triggered at {}".format(datetime.datetime.now()))


def handle_one_event(event: func.EventHubEvent):
    try:
        event_body = pickle.loads(event.get_body())
        unit_id = event_body['unit_id']
        logging.info("unitId: {}".format(unit_id))
        _, guests = mongodb_utils.query_many("guests", {"unit": unit_id})
        for guest in guests:
            guest_jwt = guest['token']
            token_valid, payload = jwt_utils.verify_jwt(guest_jwt)
            if not token_valid:
                mongodb_utils.delete_one("guests", guest)
    except Exception:
        pass