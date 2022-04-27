from cmath import log
from typing import List
import logging
import json
import azure.functions as func


def main(events: List[func.EventHubEvent], msg: func.Out[func.QueueMessage]):
    for event in events:
        logging.info('Python EventHub trigger processed an event: %s',
                        event.get_body())
        body = json.loads(event.get_body())
        logging.info(body)
        logging.info(body.keys())
        # msg.set(str(body))
        
