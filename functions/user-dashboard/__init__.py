import logging
import azure.functions as func
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt import jwt_utils
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('[Function called] User Dash Board function called.')
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}
    try:
        res_data = {}

        # get token
        token = req.headers.get("x-access-token")
        if token is None:
            res_body['message'] = "Token not provided"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # verify token and get tenant email
        token_valid, token_payload = jwt_utils.verify_jwt(token)
        if not token_valid:
            res_body['message'] = "Invalid token. Login again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        # get tenant data
        tenant_existed, tenant_data = mongodb_utils.query_one("tenants", {'email': token_payload['email']},
                                                              projections={'_id': 0, 'password': 0})
        if not tenant_existed:
            res_body['message'] = "Tenant not found"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)
        res_data['tenant'] = tenant_data

        # gather units and records data
        units_data = []
        for unit_id in tenant_data['units'].keys():
            unit_datum = {}
            unit_found, unit_data = mongodb_utils.query_one("units", {"_id": unit_id},
                                                            projections={"_id": 0})
            if not unit_found:
                continue
            unit_data['unit_id'] = unit_id
            unit_datum['unit'] = unit_data
            _, records = mongodb_utils.query_many("records", {"unit_id": unit_id},
                                                  projections={'_id': 0, "device_id": 0, "unit_id": 0},
                                                  sort_key=("timestamp", -1),
                                                  limit_num=5)
            unit_datum['records'] = records
            units_data.append(unit_datum)

        res_data['units'] = units_data
        res_body['data'] = res_data
        res_body['message'] = "Success"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)
    except Exception as ex:
        res_body['message'] = str(ex)
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
