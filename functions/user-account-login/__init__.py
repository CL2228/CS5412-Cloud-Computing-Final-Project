"""
    Log in function

    Trigger: HTTP Request
    Output: HTTP Response

    BODY: JSON
    'email': str
    'password': str

    Return: HTTP Response with JSON body
    'access-token': the token of this login operation
    'data': an object that contains the information of the account
        'email': str,
        'first_name': str,
        'last_name': str,
        'face_img': str,
        'units': an object contains basic information of a unit
            'unit_id':
                'building_name': str,
                'unit_number': str

"""

import logging
import json
import azure.functions as func

from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt.jwt_utils import generate_jwt
from ..server_functions.config import jwtLoginExpireMinutes


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("user-accout-log-in function called")

    res_body = {}
    res_headers = {'Content-Type': 'application/json'}
    try:
        req_body = req.get_json()
        email = req_body['email']
        password = req_body['password']

        query_status, query_data = mongodb_utils.query_one("tenants", {"email": email})

        # exceptions, either internal errors or user not found
        if not query_status:
            if isinstance(query_data, Exception):
                res_body['message'] = "Server Errors"
                return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
            res_body['message'] = "User not found, please register before login"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        # wrong password
        if query_data['password'] != password:
            res_body['message'] = "Wrong password"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # verification passed, generate a JWT
        token = generate_jwt({"email": email, "_id": str(query_data['_id'])}, expire_delta=jwtLoginExpireMinutes)
        res_body['access-token'] = token
        account = {'email': email,
                   'first_name': query_data['first_name'],
                   'last_name': query_data['last_name'],
                   'face_img': query_data['face_img'],
                   'units': query_data['units']}
        res_body['data'] = account
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)

    except ValueError:
        res_body['message'] = "The body of Request should be JSON!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except KeyError:
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception:
        res_body['message'] = "Internal errors"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
