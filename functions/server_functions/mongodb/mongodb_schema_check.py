"""
    MongoDB Schema Sanity Check

    [Tenant Schema]
        "email": str
        "password": str
        "first_name": str
        "last_name": str
        "face_id": str          the face ID in Azure Face
        "face_img": str         the path of support image in Blob Storage
        "units"; dict           a list of unit ID that belong to this user
                key - value : unitID - {
                                        "building_name": BUILDING_NAME,
                                        "unit_number": UNIT_NUMBER }

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
                    { email: objectID }
        "guests": dict          a dict of guests that in this unit
                    { first_name: objectID }

    [Record Schema]
        "unit": str             the Object ID of the unit that this record belongs to
        "face_id": str          the face ID of this record
        "face_img": str         the path of query image in Blob
        "verified": bool        valid verification or not
        "identity_type": str    the type of the person, can be: "tenant", "guest", "unknown"

"""


def tenant_schema_check(data: dict):
    assert "first_name" in data.keys() and type(data["first_name"]) == str
    assert "last_name" in data.keys() and type(data['last_name']) == str
    assert "email" in data.keys() and type(data['email']) == str
    assert "password" in data.keys() and type(data['password']) == str
    assert "face_id" in data.keys() and type(data['face_id']) == str or data['face_id'] is None
    assert "face_img" in data.keys() and type(data['face_img']) == str or data['face_img'] is None
    assert "units" in data.keys() and type(data['units']) == dict
    return True


def guest_schema_check(data: dict):
    assert "first_name" in data.keys() and type(data["first_name"]) == str
    assert "last_name" in data.keys() and type(data['last_name']) == str
    assert "token" in data.keys() and type(data['token']) == str
    # assert "face_id" in data.keys() and type(data['face_id']) == str
    # assert "face_img" in data.keys() and type(data['face_img']) == str
    assert "uint" in data.keys() and type(data['unit']) == str
    return True


def unit_schema_check(data: dict):
    assert "building_name" in data.keys() and type(data['building_name']) == str
    assert "address" in data.keys() and type(data['address']) == str
    assert "unit_number" in data.keys() and type(data['unit_number']) == str
    assert "tenants" in data.keys() and type(data['tenants']) == dict
    assert "guests" in data.keys() and type(data["guests"]) == dict
    return True


def record_schema_check(data: dict):
    assert "unit" in data.keys() and type(data['unit']) == str
    assert "face_id" in data.keys() and type(data['face_id']) == str
    assert "face_img" in data.keys() and type(data['face_img']) == str
    assert "verified" in data.keys() and type(data['verified']) == bool
    assert "identity_type" in data.keys() and type(data['identity_type']) in ["tenant", "guest", "unknown"]
    return True


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



