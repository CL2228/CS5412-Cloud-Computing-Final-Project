import logging
import json
import azure.functions as func
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb import mongodb_utils
import copy


def main(req: func.HttpRequest) -> func.HttpResponse:
    # response body and header
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}
    try:
        token = req.headers.get('x-access-token')
        req_body = req.get_json()

        if token is None:
            res_body['message'] = "Token missing, please log in."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        if "unit-id" not in req_body.keys():
            res_body['message'] = "Information missing, please provide access token and unit ID"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        unit_id = req_body['unit-id']

        # verify JWT
        jwt_status, jwt_payload = jwt_utils.verify_jwt(token)
        if not jwt_status:
            res_body['message'] = "Invalid token, please login again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        # retrieve user account
        user_found, user_data = mongodb_utils.query_one("tenants",
                                                        {"email": jwt_payload['email'], "_id": jwt_payload['_id']})
        if not user_found:
            res_body['message'] = "User not found, you need to log in again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        # retrieve unit data
        unit_found, unit_data = mongodb_utils.query_one("units", {"_id": unit_id})
        if not unit_found:
            res_body['message'] = "Unit not found, please make sure the unit Id is correct"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        # check if has been added before
        if unit_id in user_data['units'].keys() and str(user_data['email']) in unit_data['tenants'].keys():
            res_body['message'] = "Failed. You have already added this unit."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # update tenant
        user_units_dict = copy.deepcopy(user_data['units'])
        user_units_dict[unit_id] = {
            "building_name": unit_data['building_name'],
            "unit_number": unit_data['unit_number']
        }
        user_update_status, _ = mongodb_utils.update_one("tenants", user_data, {'units': user_units_dict})
        # update unit
        unit_tenants_dict = copy.deepcopy(unit_data['tenants'])
        unit_tenants_dict[user_data['email']] = str(user_data['_id'])
        unit_update_status, _ = mongodb_utils.update_one("units", unit_data, {'tenants': unit_tenants_dict})

        if not user_update_status or not unit_update_status:
            res_body['message'] = "Update failed. Please try again later"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)

        # succeed
        res_body['message'] = "Adding unit succeeded!"
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

