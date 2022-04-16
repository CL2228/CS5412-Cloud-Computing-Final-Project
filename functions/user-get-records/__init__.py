import logging
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt import jwt_utils


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}
    try:
        req_body = req.get_json()
        token = req.headers.get('x-access-token')
        if token is None:
            res_body['message'] = "Missing token: a JWT needs to be included in the HTTP request headers with key <x-access-token>"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        unit_id = req_body['unit-id']

        # check validity of the JWT
        jwt_valid, jwt_payload = jwt_utils.verify_jwt(token)
        if not jwt_valid:
            res_body['message'] = "Invalid token, please login (again)."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        # check whether the unit exists
        unit_existed, unit_data = mongodb_utils.query_one("units", {'_id': unit_id})
        if not unit_existed:
            res_body['message'] = "Unit doesn't exist"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        # check whether the account exists
        tenant_existed, tenant_data = mongodb_utils.query_one("tenants", {'email': jwt_payload['email']})
        if not tenant_existed:
            res_body['message'] = "Account doesn't exist."
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        # check authorization
        assert unit_id in tenant_data['units'].keys() and tenant_data['email'] in unit_data['tenants'].keys(),\
            "Not authorized to query the records of this unit"

        _, records = mongodb_utils.query_many("records", {"unit_id": unit_id},
                                              projections={"_id": 0, "unit_id": 0, "device_id": 0},
                                              sort_key=("timestamp", -1))
        print(records)
        res_body['data'] = records
        res_body['message'] = "Success"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)
    except ValueError:
        res_body['message'] = "The body of Request must be JSON!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except KeyError:
        res_body['message'] = "Missing JSON body keys, please read the instructions about how to use this api"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except AssertionError as ex:
        res_body['message'] = str(ex)
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)
    except Exception as ex:
        res_body['message'] = "Internal Errors: {}".format(str(ex))
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
