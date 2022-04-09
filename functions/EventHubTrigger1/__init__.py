from typing import List
import logging

import azure.functions as func


def main(events: List[func.EventHubEvent], msg: func.Out[func.QueueMessage]):
    for event in events:
        logging.info('Python EventHub trigger processed an event: %s',
                        event.get_body().decode('utf-8'))
        body = event.get_body().decode('utf-8')
        msg.set(str(body))
        
