"""
    create a new user (tenant) account
"""

import logging
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = {'Content-Type': 'application/json'}
    res_obj = {}

    email = req.form.get("email")
    password = req.form.get("password")
    first_name = req.form.get("first-name")
    last_name = req.form.get("last-name")
    if email is None or password is None or first_name is None or last_name is None:
        res_obj['message'] = "Please provide valid information"
        return func.HttpResponse(json.dumps(res_obj), headers=headers, status_code=400)

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
        res_obj['message'] = "Tenant schema check failed"
        return func.HttpResponse(json.dumps(res_obj), headers=headers, status_code=500)

    insert_state, insert_message = mongodb_utils.insert_with_dup_check("tenants", tenant, ['email'])
    if not insert_state:
        res_obj['message'] = insert_message
        return func.HttpResponse(json.dumps(res_obj), headers=headers, status_code=400)
    res_obj['message'] = "Successfully created your account"
    return func.HttpResponse(json.dumps(res_obj), headers=headers, status_code=200)


