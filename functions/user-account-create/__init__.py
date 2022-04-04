"""
    create a new user (tenant) account
"""

import logging
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.mongodb.mongodb_schema_check import CHECK_FUNCTIONS
from ..server_functions.jwt import jwt_utils
from ..server_functions.email import email_highlevel_helper


def send_token(req_body: dict) -> func.HttpResponse:
    """
    send token to user branch of registration
    :param req_body:
    :return:
    """
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    if "email" not in req_body.keys():
        res_body['message'] = "You need to provide an email!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    email = req_body['email']

    if mongodb_utils.check_duplicate("tenants", {'email': email}):
        res_body['message'] = "Account already existed!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    token_payload = {"email": email, "token_type": "register_token"}
    token = jwt_utils.generate_jwt(token_payload)
    email_highlevel_helper.send_token("register_token", token, email)
    res_body['message'] = "Email sent. Valid in 10 minutes"
    return func.HttpResponse(json.dumps(res_body), status_code=200, headers=res_headers)


def verify(req_body: dict) -> func.HttpResponse:
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}
    if 'email' not in req_body.keys() or 'password' not in req_body.keys() or 'token' not in req_body.keys() \
            or 'first-name' not in req_body.keys() or 'last-name' not in req_body.keys():
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    email = req_body['email']
    password = req_body['password']
    token = req_body['token']
    first_name = req_body['first-name']
    last_name = req_body['last-name']

    token_status, token_payload = jwt_utils.verify_jwt(token)
    if not token_status or token_payload['email'] != email or token_payload['token_type'] != "register_token":
        res_body['message'] = "Invalid Token"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    tenant = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "face_id": None,
        "face_img": None,
        "units": {}
    }

    if not CHECK_FUNCTIONS['tenant'](tenant):
        res_body['message'] = "Tenant schema check failed"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)

    insert_state, insert_message = mongodb_utils.insert_with_dup_check("tenants", tenant, ['email'])
    if not insert_state:
        res_body['message'] = insert_message
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    res_body['message'] = "Successfully created your account"
    return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)


def main(req: func.HttpRequest) -> func.HttpResponse:
    res_body = {}
    res_headers = {'Content-Type': 'application/json'}
    try:
        req_body = req.get_json()
        try:
            if req_body['req-type'] == "send_token":
                return send_token(req_body)
            if req_body['req-type'] == "verify":
                return verify(req_body)
        except Exception as ex:
            res_body['message'] = "Request must have a 'req-type' to indicate type"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception as ex:
        res_body['message'] = "Request must have a JSON body"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

