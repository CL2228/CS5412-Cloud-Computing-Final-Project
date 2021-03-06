"""
    Update a user's verification photo, that photo must contain a face (and only one face)

    Trigger: HTTP Request
    Output: HTTP Response

    BODY: FORM
    'img': an image file whose extension must be 'jpg', 'jpeg', 'png', server_functions/check azure_blob_helper.py for reference

    Headers:
    'x-access-token': a token for the verification of the user

"""

import logging
import azure.functions as func
import json
from io import BytesIO
from ..server_functions.blob import azure_blob_helpers
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.face import azure_face_helpers
from ..server_functions.jwt import jwt_utils


def main(req: func.HttpRequest) -> func.HttpResponse:
    # response body and header
    res_headers = {'Content-Type': 'application/json'}
    res_body = {}

    try:
        # check token and image file are provided
        img = req.files['img']
        token = req.headers.get('x-access-token')
        if token is None:
            res_body['message'] = "Token invalid. You need to login before this operation"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)
        if img is None:
            res_body['message'] = "You must provide an image"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
        img_bytes = img.read()

        # an empty file
        if len(img_bytes) == 0:
            res_body['message'] = "No file provided"
            return func.HttpResponse(json.dumps(res_body), status_code=400, headers=res_headers)

        # check uploaded file is with right format
        check_status, suffix = azure_blob_helpers.check_img_file_suffix(img.filename)
        if not check_status:
            res_body['message'] = "Unsupported file format"
            return func.HttpResponse(json.dumps(res_body), status_code=400, headers=res_headers)

        # verify JWT
        jwt_status, jwt_payload = jwt_utils.verify_jwt(token)
        if not jwt_status:
            res_body['message'] = "Invalid token, you need to log in again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=401)

        # get account info from cosmosDB
        account_status, account = mongodb_utils.query_one("tenants", {'email': jwt_payload['email']})
        if not account_status:
            res_body['message'] = "Account not found, please log in again to verify"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=404)
        
        # detect face and get faceID
        face_detect_status, face_id = azure_face_helpers.get_faceId_with_stream(BytesIO(img_bytes))
        # if not face detected
        if not face_detect_status:
            res_body['message'] = face_id
            return func.HttpResponse(json.dumps(res_body), status_code=403, headers=res_headers)

        # upload the image to Blob
        old_img_blob = account['face_img']
        new_img_blob = azure_blob_helpers.generate_file_name(prefix="tenants/" + str(account['_id']) + "/", suffix="." + suffix)
        blob_upload_status, blob_upload_message = azure_blob_helpers.write_blob(new_img_blob, BytesIO(img_bytes),
                                                                                content_type='image/jpeg')
        if not blob_upload_status:
            res_body['message'] = "Internal fail"
            return func.HttpResponse(json.dumps(res_body), status_code=500, headers=res_headers)

        # update account information in cosmosDB
        update_data = {'face_img': new_img_blob}
        update_status, _ = mongodb_utils.update_one("tenants", account, update_data)
        if not update_status:
            azure_blob_helpers.delete_blob(new_img_blob)
            res_body['message'] = "Update failed, please try again"
            return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)

        # update successfully, now delete old image in the Blob
        # delete_status, _ = azure_blob_helpers.delete_blob(old_img_blob)

        res_body['message'] = "Update personal verification photo successfully"
        return func.HttpResponse(json.dumps(res_body), status_code=200, headers=res_headers)
    except KeyError as ex:
        res_body['message'] = "Missing keys. Please check the validity of requests"
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=400)
    except Exception as ex:
        res_body['message'] = str(ex)
        return func.HttpResponse(json.dumps(res_body), headers=res_headers, status_code=500)


