"""
 This function is for removing a tenant from a unit

    Request
        Headers:
            'x-access-token': the login token of a manager's account
        Body(JSON):
            'tenant-email': the email of the tenant's account
            'unit-id': the unit ID of the building
"""
import copy
import logging
import json
import azure.functions as func
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb import mongodb_utils


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

        # check if tenant or unit exists
        tenant_existed, tenant_data = mongodb_utils.query_one("tenants", {"email": req_body['tenant-email']})
        if not tenant_existed:
            res_body['message'] = "Tenant doesn't exist."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)
        unit_existed, unit_data = mongodb_utils.query_one("units", {"_id": req_body['unit-id']})
        if not unit_existed:
            res_body['message'] = "Unit doesn't exist."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        # update tenant and unit data
        tenant_unit_dict = dict(copy.deepcopy(tenant_data['units']))
        tenant_unit_dict.pop(req_body['unit-id'], None)
        unit_tenant_dict = dict(copy.deepcopy(unit_data['tenants']))
        unit_tenant_dict.pop(req_body['tenant-email'], None)
        tenant_update_status, tenant_update_msg = mongodb_utils.update_one("tenants", tenant_data,
                                                                           {"units": tenant_unit_dict})
        unit_update_status, unit_update_msg = mongodb_utils.update_one("units", unit_data,
                                                                       {"tenants": unit_tenant_dict})
        if not tenant_update_status or not unit_update_status:
            logging.error(tenant_update_msg)
            logging.error(unit_update_msg)
            res_body['message'] = "Update error. Please try again."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=403)
        res_body['message'] = "Updated successfully."
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
