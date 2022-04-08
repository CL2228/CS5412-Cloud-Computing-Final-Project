from typing import List
import logging
import pickle
import azure.functions as func


def main(events: List[func.EventHubEvent]):
    for event in events:
        event_body = pickle.loads(event.get_body())
        logging.info('Python EventHub trigger processed an event: %s',
                        event.get_body())
        # print(event_body)
