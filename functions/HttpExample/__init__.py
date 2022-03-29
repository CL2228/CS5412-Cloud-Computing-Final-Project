import logging

import azure.functions as func

from ..server_functions import azure_blob_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    #
    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )

    data_status, data = azure_blob_helpers.read_blob("test-container", "test.jpg")
    if not data_status:
        return func.HttpResponse("Data not found", status_code=404)

    header = {'Content-Type': 'image/jpeg'}
    response = func.HttpResponse(data, status_code=200, headers=header)
    return response
