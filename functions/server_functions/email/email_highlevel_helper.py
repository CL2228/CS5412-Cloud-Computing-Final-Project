import datetime
import logging

from ..email import email_utils
from .email_config import EMAIL_SUBJECTS, EMAIL_BODIES, ALLOW_TYPES
from ..config import imgBaseUrl
from ..blob import azure_blob_helpers

def send_token(msg_type: str, token: str, email_to: str):
    assert msg_type in ALLOW_TYPES
    msg = EMAIL_BODIES[msg_type].format(email_to, token)
    email_utils.send_plain_text(subject=EMAIL_SUBJECTS[msg_type], to=email_to, content=msg)


def send_warning_email(email_to: str,
                       unit_data: dict,
                       verification_result: dict):
    blob_found, blob_data = azure_blob_helpers.read_blob(verification_result['blob_name'])
    if not blob_found:
        logging.error("Blob not found")
        return

    msg = EMAIL_BODIES['warning_html'].format(unit_data['unit_number'], unit_data['building_name'],
                                              datetime.datetime.fromtimestamp(verification_result['timestamp']))
    email_utils.send_html(subject=EMAIL_SUBJECTS['warning_record'], to=email_to, html_content=msg, img_bytes=blob_data)


if __name__ == "__main__":
    send_token("retrieve_token",
               "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNsMjIyOEBjb3JuZWxsLmVkdSIsIl9pZCI6IjYyNDc2NjZhNDg5MThmMmY4YTRmNGRhZCIsImV4cCI6MTY0OTAzMTYwM30.Dmg2YpfmfeSrc55nB3Bp7KKn0xDztCY74bS5oC_Efwc",
               "cl2228@cornell.edu")
