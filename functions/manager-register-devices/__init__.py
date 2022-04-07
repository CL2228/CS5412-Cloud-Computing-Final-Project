"""
    Register a new IOT device for the system, and blind it with a unit
"""
import azure.functions as func
import json
from ..server_functions.mongodb import mongodb_utils


def main(req: func.HttpRequest) -> func.HttpResponse:
    res_body = {}
    res_headers = {'Content-Type': 'application/json'}
    try:
        req_body = req.get_json()
        device_key = req_body['azure-iothub-device-key']
        unit_id = req_body['unit-id']

        unit_found, _ = mongodb_utils.query_one("units", {'_id': unit_id})
        if not unit_found:
            res_body['message'] = "Unit not found, please check the ID again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)

        device_found, device_data = mongodb_utils.query_one("devices", {'device_key': device_key})
        if device_found:
            insert_status, _ = mongodb_utils.update_one("devices", device_data, {"unit_id": unit_id})
        else:
            device_data = {"devices_key": device_key, "unit_id": unit_id}
            insert_status, _ = mongodb_utils.insert("devices", device_data)
        if not insert_status:
            res_body['message'] = "Internal errors. Please try again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)
        res_body['message'] = "Updated successfully"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)

    except ValueError:
        res_body['message'] = "The body of the request must be JSON!"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except KeyError:
        res_body['message'] = "Missing information"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception:
        res_body['message'] = "Internal errors"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)

