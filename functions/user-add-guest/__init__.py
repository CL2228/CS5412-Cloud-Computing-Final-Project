import json
import logging
import azure.functions as func
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.blob import azure_blob_helpers


def main(req: func.HttpRequest) -> func.HttpResponse:
    # response body and header
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    # get token and the unit ID
    token = req.headers.get('x-access-token')
    req_body = req.get_json()
    unit_id = req_body['uint']
    if token is None or unit_id is None:
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    # check validity of JWT
    jwt_status, jwt_payload = jwt_utils.verify_jwt(token)
    if not jwt_status:
        res_body['message'] = "Token invalid. Please login"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)



