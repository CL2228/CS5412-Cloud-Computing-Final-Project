from cmath import log
from typing import List
import logging
import azure.functions as func
import pickle


def main(events: List[func.EventHubEvent]):
    for event in events:
        event_body = pickle.loads(event.get_body())
        # logging.info('Python EventHub trigger processed an event: %s',
        #                 event.get_body())
        # body = pickle.loads(body)
        logging.info("Test output-----------------")
        logging.info(event_body)

