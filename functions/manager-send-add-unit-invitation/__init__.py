import logging
import json
import azure.functions as func
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.email import email_highlevel_helper
from ..server_functions.config import jwtNewTenantRegisterExpireMinutes


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # response body and headers
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    try:
        token = req.headers.get('x-access-token')
        req_body = req.get_json()

        # get token
        if token is None:
            res_body['message'] = "Token missing, please log in."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        # check required fields
        if "tenant-email" not in req_body.keys() or "unit-id" not in req_body.keys():
            res_body['message'] = "Information missing"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # check if token expires
        token_valid, token_payload = jwt_utils.verify_jwt(token)
        if not token_valid:
            res_body['message'] = "Invalid token"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)
        # check if it belongs to a manager
        if "email" not in token_payload.keys() or token_payload['email'] != "cl2228@cornell.edu":
            res_body['message'] = "This token must belong to a manager."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=403)

        # check if unit exists and this account doesn't belong to that unit
        unit_existed, unit_data = mongodb_utils.query_one("units", {"_id": req_body['unit-id']})
        if not unit_existed:
            res_body['message'] = "Unit doesn't exist."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)
        if req_body['tenant-email'] in unit_data['tenants'].keys():
            res_body['message'] = "This unit has already been added to this account."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        new_token_payload = {"email": req_body['tenant-email'], 'unit_id': req_body['unit-id']}
        new_token = jwt_utils.generate_jwt(new_token_payload, jwtNewTenantRegisterExpireMinutes)
        email_highlevel_helper.send_new_tenant_invitation(new_token, unit_data, req_body['tenant-email'])
        res_body['message'] = "Successfully sent invitation"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)
    except ValueError as ex:
        logging.error(ex)
        res_body['message'] = "The body of Request should be JSON!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except KeyError as ex:
        logging.error(ex)
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception as ex:
        logging.error(ex)
        res_body['message'] = 'Internal errors'
        return func.HttpResponse(json.dumps(res_body), status_code=500, headers=res_headers)
