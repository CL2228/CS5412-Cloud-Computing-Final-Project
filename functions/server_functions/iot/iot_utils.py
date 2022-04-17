from azure.iot.hub import IoTHubRegistryManager
from ..config import azureIotHubConnectString
# from functions.server_functions.config import azureIotHubConnectString
import json


def send_message_to_device(device_id: str, payload: dict):
    """
    send a message to an IOT device
    :param device_id: the device ID in IoT Hub
    :param payload: the payload of data, is must be a dict. This dict will be turned into string with json
    :return: [T / F, message]
    """
    try:
        registry_manager = IoTHubRegistryManager(azureIotHubConnectString)
        props = {}
        props.update(contentType="application/json")
        payload = json.dumps(payload)
        registry_manager.send_c2d_message(device_id, payload, properties=props)
        return True, "Success"
    except Exception as ex:
        return False, ex


if __name__ == "__main__":
    pl = {"name": "cli"}
    device_id = "gates-hall-g01"
    print(send_message_to_device(device_id, pl))
