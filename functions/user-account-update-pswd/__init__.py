import logging
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt import jwt_utils
from ..server_functions.email import email_highlevel_helper


def send_token(req_body: dict) -> func.HttpResponse:
    res_body = {}
    res_headers = {'Content-Type': 'application/json'}
    if "email" not in req_body.keys():
        res_body['message'] = "You need to provide an email!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    email = req_body['email']

    if not mongodb_utils.check_duplicate("tenants", {"email": email}):
        res_body['message'] = "Account doesn't exist!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

    token_payload = {"email": email, "token_type": "retrieve_token"}
    token = jwt_utils.generate_jwt(token_payload)
    email_highlevel_helper.send_token("retrieve_token", token, email)
    res_body['message'] = "Email sent. Valid in 10 minutes"
    return func.HttpResponse(json.dumps(res_body), status_code=200, headers=res_headers)


def verify(req_body: dict) -> func.HttpResponse:
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    if 'email' not in req_body.keys() or 'new-password' not in req_body.keys() or 'token' not in req_body.keys():
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    email = req_body['email']
    new_password = req_body['new-password']
    token = req_body['token']

    token_status, token_payload = jwt_utils.verify_jwt(token)
    if not token_status or "token_type" not in token_payload.keys() or token_payload['token_type'] != "retrieve_token" \
            or "email" not in token_payload.keys() or token_payload['email'] != email:
        res_body['message'] = "Invalid token, please try again"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

    account_status, account_data = mongodb_utils.query_one("tenants", {'email': email})
    if not account_status:
        res_body['message'] = "Account doesn't exist"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    update_data = {"password": new_password}
    update_status, update_message = mongodb_utils.update_one("tenants", account_data, update_data)
    if not update_status:
        res_body['message'] = "Update failed, please try again. This may because concurrent modifications happened."
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
    res_body['message'] = update_message
    return func.HttpResponse(json.dumps(res_body), status_code=200, headers=res_headers)


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
            res_body['message'] = "Invalid request type"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        except Exception:
            res_body['message'] = "Request must have a 'req-type' to indicate type"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except ValueError:
        res_body['message'] = "Request must have a JSON body"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception as ex:
        res_body['message'] = str(ex)
        return func.HttpResponse(json.dumps(res_body), status_code=500, headers=res_headers)




