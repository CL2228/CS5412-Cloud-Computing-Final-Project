"""
    This is the function that send telemetries to IoT device to notify the verification result

    the payload of the telemetry is a dict that contains:

    "verified": bool
    "timestamp: float
"""
import datetime
from typing import List
import logging
from ..server_functions.iot import iot_utils
import azure.functions as func
import pickle


def main(events: List[func.EventHubEvent],
         outputQueueItem: func.Out[func.QueueMessage]):
    for event in events:
        logging.info('[Event function triggered]Core-notify-iot-device, with payload:{}'.format(pickle.loads(event.get_body())))
        res = handle_one_event(event)
        outputQueueItem.set("Event processed at: {}, result:{}".format(datetime.datetime.now(), res))


def handle_one_event(event: func.EventHubEvent):
    try:
        event_body = pickle.loads(event.get_body())
        payload = {"verified": event_body['verified'],
                   "timestamp": event_body['timestamp']}
        # use IOT module to send a command to the IoT devices.
        iot_utils.send_message_to_device(event_body['device_id'], payload)
        return True, "Success"
    except Exception as ex:
        return False, ex
