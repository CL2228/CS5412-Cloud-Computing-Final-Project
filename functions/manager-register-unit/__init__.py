import logging
import json
import azure.functions as func
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('[Manager-register-unit] function triggered.')

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

        # check request field
        if "building-name" not in req_body.keys() or "address" not in req_body.keys() \
                or "unit-number" not in req_body.keys():
            res_body['message'] = "Information missing."
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

        # construct unit data
        unit_data = {
            "building_name": req_body['building-name'],
            "address": req_body['address'],
            "unit_number": req_body['unit-number'],
        }
        if mongodb_utils.check_duplicate("units", unit_data):
            res_body['message'] = "This unit already existed"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=403)
        unit_data['tenants'] = {}
        CHECK_FUNCTIONS['unit'](unit_data)
        insert_res, _ = mongodb_utils.insert("units", unit_data)
        if not insert_res:
            res_body['message'] = "Insertion error. Please try again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
        res_body['message'] = "Successfully added"
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
