import logging

import azure.functions as func
from ..server_functions import azure_blob_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    file = req.files['f1']
    logging.info("\n\n")
    logging.info(file)
    logging.info(file.filename)
    logging.info("\n\n")

    state, message = azure_blob_helpers.write("test-container", "test.jpg", file, 'image/jpeg')
    if state:
        return func.HttpResponse("Uploaded successfully")
    else:
        return func.HttpResponse(f"Upload failed{message}")