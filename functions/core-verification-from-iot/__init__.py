from typing import List
import logging
import azure.functions as func
import pickle
from ..server_functions.face import azure_face_helpers
from ..server_functions.mongodb import mongodb_utils
from ..server_functions.jwt import jwt_utils
from ..server_functions.blob import azure_blob_helpers
from io import BytesIO


def main(events: List[func.EventHubEvent],
         writeRecordEventHub: func.Out[bytes],
         sendEmailEventHub: func.Out[bytes],
         notifyIotEventHub: func.Out[bytes],
         garbageCollectionUnitEventHub: func.Out[bytes],
         msg: func.Out[func.QueueMessage]):
    for event in events:
        body = dict(pickle.loads(event.get_body()))
        logging.info('[Event triggered]Core-verification-from-iot, with payload: {}'.format(body))
        res_body = handle_one_event(event)

        if type(res_body) != dict:
            msg.set(str(res_body))
            continue
        msg.set(res_body['verify_identity'])

        writeRecordEventHub.set(pickle.dumps(res_body))
        garbageCollectionUnitEventHub.set(pickle.dumps({"unit_id": res_body['unit_id']}))
        notifyIotEventHub.set(pickle.dumps(res_body))
        if not res_body['verified']:
            sendEmailEventHub.set(pickle.dumps(res_body))
        logging.info("RESULT---------------------------------------")
        logging.info(res_body)


def handle_one_event(event: func.EventHubEvent):
    """
    handle an event in the event-hub "verification-request-event"

    :param event: an EventHubEvent object
    :return: a dict object that records the result (if there is no internal error)
                otherwise return exceptions
    """
    res_body = {'timestamp': event.enqueued_time.timestamp(),
                'unit_id': "",
                'device_id': "",
                'blob_name': "",
                'verified': False,
                "verify_identity": "",
                "reference_img": None,
                "confidence": 0.0}
    try:
        # basic response body
        body = dict(pickle.loads(event.get_body()))
        res_body['blob_name'] = body['blob_name']

        # retrieve device data from database to decide which unit to detect
        device_existed, device_data = mongodb_utils.query_one("devices", {"device_key": body['device_key']})
        if not device_existed:
            logging.error("IoT device not found")
            return "IoT device not found"
        unit_id = device_data['unit_id']
        res_body['unit_id'] = unit_id
        res_body['device_id'] = device_data['device_id']

        # get query face
        query_img_steam = BytesIO(azure_blob_helpers.read_blob(body['blob_name'])[1])
        query_face_detected, query_face_id = azure_face_helpers.get_faceId_with_stream(query_img_steam)
        if not query_face_detected:
            res_body['verify_identity'] = "Face not detected"
            return res_body

        # get unit information
        unit_found, unit_data = mongodb_utils.query_one("units", {'_id': unit_id})
        if not unit_found:
            logging.error("Unit not found")
            return "Unit not found"

        # get tenants associated with the unit and check if this person is a tenant
        tenants = unit_data['tenants']
        for tenant_email in tenants.keys():
            tenant_found, tenant_data = mongodb_utils.query_one("tenants", {'email': tenant_email})
            if not tenant_found or tenant_data['face_img'] is None:
                continue
            logging.info("----------tenant_img:{}".format(tenant_data['face_img']))
            tenant_img_stream = BytesIO(azure_blob_helpers.read_blob(tenant_data['face_img'])[1])
            tenant_face_detected, tenant_face_id = azure_face_helpers.get_faceId_with_stream(tenant_img_stream)
            if not tenant_face_detected:
                continue
            verify_res, verify_confidence = azure_face_helpers.verify_two_faces(query_face_id, tenant_face_id)
            if verify_res:
                res_body['verified'] = True
                res_body['confidence'] = verify_confidence
                res_body['verify_identity'] = "tenant: {}".format(tenant_data['first_name'] + " " + tenant_data['last_name'])
                res_body['reference_img'] = tenant_data['face_img']
                return res_body

        # check guests of this unit
        guest_existed, guests = mongodb_utils.query_many("guests", {"unit": unit_id})
        if guest_existed:
            for guest in guests:
                guest_token = guest['token']
                guest_token_valid, guest_token_payload = jwt_utils.verify_jwt(guest_token)
                if not guest_token_valid:
                    continue
                guest_face_id = guest_token_payload['face_id']
                verify_res, verify_confidence = azure_face_helpers.verify_two_faces(query_face_id, guest_face_id)
                if verify_res:
                    res_body['verified'] = True
                    res_body['confidence'] = verify_confidence
                    res_body['verify_identity'] = "guest: {}".format(guest['first_name'] + " " + guest['last_name'])
                    res_body['reference_img'] = guest_token_payload['face_img']
                    return res_body

        res_body['verify_identity'] = "Stranger"
        return res_body
    except KeyError as ex:
        logging.error(ex)
        return str(ex)
    except Exception as ex:
        logging.error(ex)
        return str(ex)
