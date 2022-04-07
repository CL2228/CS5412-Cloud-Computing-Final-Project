import logging

import azure.functions as func


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')
    req_body = dict(req.get_json())
    msg = req_body['message']
    return msg
    
