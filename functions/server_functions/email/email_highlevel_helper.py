import datetime

from ..email import email_utils
from .email_config import EMAIL_SUBJECTS, EMAIL_BODIES, ALLOW_TYPES
from ..mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def send_token(msg_type: str, token: str, email_to: str):
    assert msg_type in ALLOW_TYPES
    msg = EMAIL_BODIES[msg_type].format(email_to, token)
    email_utils.send(subject=EMAIL_SUBJECTS[msg_type], to=email_to, content=msg)


def send_warning_email(email_to: str,
                       unit_data: dict,
                       timestamp):
    msg = EMAIL_BODIES['warning_record'].format(email_to,
                                                unit_data['unit_number'],
                                                unit_data['building_name'],
                                                datetime.datetime.fromtimestamp(timestamp))
    email_utils.send(subject=EMAIL_SUBJECTS['warning_record'], to=email_to, content=msg)


if __name__ == "__main__":
    send_token("retrieve_token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNsMjIyOEBjb3JuZWxsLmVkdSIsIl9pZCI6IjYyNDc2NjZhNDg5MThmMmY4YTRmNGRhZCIsImV4cCI6MTY0OTAzMTYwM30.Dmg2YpfmfeSrc55nB3Bp7KKn0xDztCY74bS5oC_Efwc", "cl2228@cornell.edu")