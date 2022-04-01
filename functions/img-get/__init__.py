import logging
import azure.functions as func
import json
from ..server_functions.blob import azure_blob_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    res_headers = {'Content-Type': 'application/json'}
    if not name:
        return func.HttpResponse(json.dumps({"message": "wrong request params"}),
                                 status_code=400,
                                 headers=res_headers)

    read_status, read_data = azure_blob_helpers.read_blob(name)
    if not read_status:
        if read_data == "Blob doesn't exist":
            return func.HttpResponse(json.dumps({'message': 'Data not found'}),
                                     status_code=404,
                                     headers=res_headers)
        else:
            return func.HttpResponse(json.dumps({'message': "Internal errors"}),
                                     status_code=500,
                                     headers=res_headers)

    res_headers['Content-Type'] = 'image/jpeg'
    return func.HttpResponse(read_data, status_code=200, headers=res_headers)


