import logging
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    res_body = {}
    res_headers = {'Content-Type': 'application/json'}

    email = req.form.get("email")
    old_password = req.form.get("old-password")
    new_password = req.form.get("new-password")

    if email is None or old_password is None or new_password is None:
        res_body['message'] = "Please provide email and password"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    query_status, query_data = mongodb_utils.query_one("tenants", {"email": email})

    # exceptions, either internal errors or user not found
    if not query_status:
        if isinstance(query_data, Exception):
            res_body['message'] = "Server Errors"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
        res_body['message'] = "User not found, please register before login"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

    # wrong password
    if query_data['password'] != old_password:
        res_body['message'] = "Wrong old password"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    update_data = {"password": new_password}
    update_status, update_message = mongodb_utils.update_one("tenants", query_data, update_data)
    res_body['message'] = update_message
    if not update_status:
        return func.HttpResponse(json.dumps(res_body), status_code=400, headers=res_headers)
    return func.HttpResponse(json.dumps(res_body), status_code=200, headers=res_headers)



