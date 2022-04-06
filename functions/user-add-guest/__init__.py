import json
import logging
import azure.functions as func
from io import BytesIO
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.blob import azure_blob_helpers
from ..server_functions.face import azure_face_helpers
from ..server_functions.config import jwtGuestExpireMinutes
from ..server_functions.jwt import jwt_utils
from ..server_functions.mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def main(req: func.HttpRequest) -> func.HttpResponse:
    # response body and header
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    try:
        # get token and the unit ID
        token = req.headers.get('x-access-token')
        if token is None:
            res_body['message'] = "Missing information"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # check validity of JWT
        jwt_status, jwt_payload = jwt_utils.verify_jwt(token)
        if not jwt_status:
            res_body['message'] = "Token invalid. Please login"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)

        # check if there is information missing
        img = req.files['img']
        first_name = req.form.get('first-name')
        last_name = req.form.get('last-name')
        unit_id = req.form.get('unit-id')
        if img is None or first_name is None or last_name is None or unit_id is None:
            res_body['message'] = "Information missing"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        img_bytes = img.read()

        # check uploaded file is with right format
        check_status, suffix = azure_blob_helpers.check_img_file_suffix(img.filename)
        if not check_status:
            res_body['message'] = "Unsupported file format"
            return func.HttpResponse(json.dumps(res_body), status_code=400, headers=res_headers)

        # get the tenant data
        tenant_found, tenant_data = mongodb_utils.query_one("tenants", {'email': jwt_payload['email'], '_id': jwt_payload['_id']})
        if not tenant_found:
            res_body['message'] = "Tenant data not found, please log in again"
            return func.HttpResponse(json.dumps(res_body), status_code=404, headers=res_headers)

        # get the unit data
        unit_found, unit_data = mongodb_utils.query_one("units", {'_id': unit_id})
        if not unit_found:
            res_body['message'] = "Unit not found"
            return func.HttpResponse(json.dumps(res_body), status_code=404, headers=res_headers)

        # this tenant doesn't belong to the unit
        if unit_id not in tenant_data['units'].keys() or tenant_data['email'] not in unit_data['tenants'].keys():
            res_body['message'] = "You have no right to ad guests to this unit"
            return func.HttpResponse(json.dumps(res_body), status_code=403, headers=res_headers)

        # now passed the authorization
        # detect face and get face ID
        face_detect_status, face_id = azure_face_helpers.get_faceId_with_stream(BytesIO(img_bytes))
        if not face_detect_status:
            res_body['message'] = face_id
            return func.HttpResponse(json.dumps(res_body), status_code=400, headers=res_headers)

        # upload the image to Blob
        img_name = azure_blob_helpers.generate_file_name(suffix="." + suffix, prefix="guests/" + str(unit_data['_id']) + "/")
        blob_upload_status, blob_upload_message = azure_blob_helpers.write_blob(img_name,
                                                                                BytesIO(img_bytes),
                                                                                content_type='image/jpeg')
        if not blob_upload_status:
            res_body['message'] = "Internal error, image uploading failed"
            return func.HttpResponse(json.dumps(res_body), status_code=500, headers=res_headers)

        # format data for the guest
        token = jwt_utils.generate_jwt({'face_id': str(face_id), "face_img": img_name}, jwtGuestExpireMinutes)
        guest_data = {
            "first_name": first_name,
            "last_name": last_name,
            "token": token,
            "unit": unit_id
        }
        CHECK_FUNCTIONS['guest'](guest_data)

        # insert
        guest_insert_status, _ = mongodb_utils.insert("guests", guest_data)
        if not guest_insert_status:
            azure_blob_helpers.delete_blob(img_name)
            res_body['message'] = "Data insertion failed, please try again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)

        # succeed
        res_body['message'] = "Adding guest succeeded."
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=200)

    except KeyError as ex:
        res_body['message'] = "Missing keys. Please check the validity of requests"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception:
        res_body['message'] = "Internal errors"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)



