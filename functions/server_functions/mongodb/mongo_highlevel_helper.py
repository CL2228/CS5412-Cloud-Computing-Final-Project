from ..mongodb import mongodb_utils
from ..mongodb.mongodb_schema_check import CHECK_FUNCTIONS


def insert_unit(building_name: str,
                address: str,
                unit_number: str,
                tenants: dict):
    """
    insert a piece of unit data to mongoDB
    :param building_name: the name of the building
    :param address: the address
    :param unit_number: unit number
    :param tenants: a dict that contains the tenants of this unit, check mongo_schema_check.py for the format of data
    :return: [T / F, message]
    """
    data = {
        "building_name": building_name,
        "address": address,
        "unit_number": unit_number,
        "tenants": tenants
    }
    CHECK_FUNCTIONS['unit'](data)

    if mongodb_utils.check_duplicate("units", data):
        return False, "Unit already existed"

    return mongodb_utils.insert("units", data)


def check_authorization(unit_data: dict,
                        tenant_data: dict) -> bool:
    """
        check if a tenant has access to a unit
    :param unit_data: the data of a unit from mongoDB
    :param tenant_data: the data of a tenant from mongoDB
    :return:  T / F
    """
    try:
        unit_id = str(unit_data['_id'])
        tenant_email = str(tenant_data['email'])
        return unit_id in tenant_data['units'].keys() and tenant_email in unit_data['tenants'].keys()
    except Exception:
        return False


if __name__ == "__main__":
    print(insert_unit("GatesHall", "Cornell University", "G01", {}))
