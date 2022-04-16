"""
    MongoDB Schema Sanity Check

    [Tenant Schema]
        "email": str
        "password": str
        "first_name": str
        "last_name": str
        "face_img": str         the path of support image in Blob Storage
        "units"; dict           a list of unit ID that belong to this user
                key - value : unitID - {
                                        "building_name": BUILDING_NAME,
                                        "unit_number": UNIT_NUMBER
                                        }

    [Guest Schema]
        "first_name": str
        "last_name": str
        "token": str,           a token whose payload contains the
                                    { "face_id", "face_img" }
        "unit": str

    [Unit Schema]
        "building_name": str
        "address": str
        "unit_number": str
        "tenants": dict         a dict of tenants that in this unit
                    { email: objectID
                    }


    [Record Schema]
        "timestamp": double    the time stamp of the record
        "unit_id": str          the Object ID of the unit that this record belongs to
        "face_img": str         the blob name of query image
        "device_id": str        the device ID of the IoT device
        "ref_img": str          the blob name of support image (if exists)
        "verified": bool        valid verification or not
        "verify_identity": str  the identification of that record (could be tenant's name, "Guest" or "Stranger"
"""


def tenant_schema_check(data: dict):
    assert "first_name" in data.keys() and type(data["first_name"]) == str, "Wrong first name info"
    assert "last_name" in data.keys() and type(data['last_name']) == str, "Wrong lasts name info"
    assert "email" in data.keys() and type(data['email']) == str, "Wrong email info"
    assert "password" in data.keys() and type(data['password']) == str, "Wrong password info"
    assert "face_img" in data.keys() and type(data['face_img']) == str or data['face_img'] is None, "Wrong face image info"
    assert "units" in data.keys() and type(data['units']) == dict, "Wrong units info"


def guest_schema_check(data: dict):
    assert "first_name" in data.keys() and type(data["first_name"]) == str, "Wrong first name info"
    assert "last_name" in data.keys() and type(data['last_name']) == str, "Wrong last name info"
    assert "token" in data.keys() and type(data['token']) == str, "Wrong token type"
    assert "unit" in data.keys() and type(data['unit']) == str, "Wrong unit type"


def unit_schema_check(data: dict):
    assert "building_name" in data.keys() and type(data['building_name']) == str, "Wrong building name info"
    assert "address" in data.keys() and type(data['address']) == str, "Wrong address info"
    assert "unit_number" in data.keys() and type(data['unit_number']) == str, "Wrong unit number info"
    assert "tenants" in data.keys() and type(data['tenants']) == dict, "Wrong tenants info"


def record_schema_check(data: dict):
    assert "timestamp" in data.keys(), "Wrong timestamp info"
    assert "unit_id" in data.keys() and type(data['unit_id']) == str, "Wrong unit id info"
    assert "face_img" in data.keys() and type(data['face_img']) == str, "Wrong face image info"
    assert "device_id" in data.keys() and type(data['device_id']) == str, "Wrong device ID info"
    assert "ref_img" in data.keys() and data['ref_img'] is None or type(data['ref_img']) == str, "Wrong reference image info"
    assert "verified" in data.keys() and type(data['verified']) == bool, "Wrong verified info"
    assert "verify_identity" in data.keys() and type(data['verify_identity']) == str, "Wrong verify identity info"


CHECK_FUNCTIONS = {
    "tenant": tenant_schema_check,
    "guest": guest_schema_check,
    "unit": unit_schema_check,
    "record": record_schema_check,
}


if __name__ == "__main__":
    tenant = {
        "email": "w",
        "first_name": "Chenghui",
        "last_name": "erw",
        "face_id": None,
        "face_img": None,
        "units": []
    }
    a = []
    print(type(a))
    try:
        tenant_schema_check(tenant)
        print("passed")
    except AssertionError as ex:
        print("wrong format")



