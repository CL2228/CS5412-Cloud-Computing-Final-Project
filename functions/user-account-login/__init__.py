import logging
import json
import azure.functions as func

from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt.jwt_utils import generate_jwt


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("user-accout-log-in function called")

    res_body = {}
    res_headers = {'Content-Type': 'application/json'}

    email = req.form.get("email")
    password = req.form.get("password")

    if email is None or password is None:
        res_body['message'] = "Please provide email and password"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    query_status, query_data = mongodb_utils.query_one("tenants", {"email": email})
    
    logging.info("status: {};  data:{}".format(query_status, query_data))

    # exceptions, either internal errors or user not found
    if not query_status:
        if isinstance(query_data, Exception):
            res_body['message'] = "Server Errors"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
        res_body['message'] = "User not found, please register before login"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

    # wrong answer
    if query_data['password'] != password:
        res_body['message'] = "Wrong password"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

    logging.info(str(query_data['_id']))

    # verification passed, generate a JWT
    token = generate_jwt({"email": email, "_id": str(query_data['_id'])})
    res_body['access-token'] = token
    account = {'email': email,
               'first_name': query_data['first_name'],
               'last_name': query_data['last_name'],
               'face_img': query_data['face_img'],
               'units': query_data['units']}
    res_body['data'] = account
    return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)

























