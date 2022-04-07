import mongodb_utils
from mongodb_schema_check import CHECK_FUNCTIONS


def insert_unit(building_name: str,
                address: str,
                unit_number: str,
                tenants: dict):
    """
    insert a piece of unit data to mongoDB
    :param building_name:
    :param address:
    :param unit_number:
    :param tenants:
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


if __name__ == "__main__":
    print(insert_unit("GatesHall", "Cornell University", "G01", {}))
