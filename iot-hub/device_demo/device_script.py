import asyncio
import datetime
import os
import time
import uuid
import json
import azure.iot.device.exceptions
from azure.iot.device.aio import IoTHubDeviceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContentSettings
import event_hub_helper

DEVICE_CONN_STR = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=gates-hall-g01;SharedAccessKey=ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="
DEVICE_KEY = "ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="
EVENT_HUB_NAME = "verification-request-event"

########################################################
# Utils
########################################################
def check_img_file_suffix(filename: str):
    """
        check image format
    :param filename: [T / F, suffix without '.' / message]
    :return:
    """
    try:
        img_extensions = {'jpg', 'png', 'jpeg'}
        suffix = filename.rsplit('.', 1)[1].lower()
        if '.' not in filename or suffix not in img_extensions:
            return False, "File format not allowed"
        return True, suffix
    except Exception as ex:
        return False, ex


def generate_file_name(prefix: str = None, suffix: str = None):
    """
        generate unique name for blob
    :param prefix: prefix of the file name, usually the path of that file
    :param suffix: the suffix of the file
    :return: unique names
    """
    name = str(uuid.uuid4())
    if prefix is not None:
        name = prefix + name
    if suffix is not None:
        name += suffix
    return name


########################################################
# Receive messages from Azure cloud
########################################################
def message_handler(message):
    print("\n---------------------------------------------------------------")
    print("New message received from cloud at {}".format(datetime.datetime.now()))
    print("-----Message Metadata:")
    for prop in vars(message).items():
        print("    {}".format(prop))
    print("-----Metadata end.")
    print("-----Message payload:")
    data = vars(message)['data']
    data = json.loads(data)
    print(data)
    print("---------------------------------------------------------------\n")


########################################################
# Receive messages from Azure cloud
########################################################
async def trigger_verification_request(img_path: str, device_key, device_client: IoTHubDeviceClient):
    try:
        print("\n\nVerification process starting at{}...".format(datetime.datetime.now()))
        print("Checking image file format...")
        check_img, suffix = check_img_file_suffix(img_path)
        if not check_img:
            raise Exception("[ERROR] Invalid image path")

        print("Image format check passed, creating blob info...")
        blob_name = generate_file_name(prefix="records/", suffix="." + suffix)
        storage_info = await device_client.get_storage_info_for_blob(blob_name)
        sas_url = "https://{}/{}/{}{}".format(
            storage_info['hostName'],
            storage_info['containerName'],
            storage_info['blobName'],
            storage_info['sasToken']
        )
        print("Blob information: {}".format(storage_info))

        print("Uploading image...")
        with BlobClient.from_blob_url(sas_url) as blob_client:
            with open(img_path, "rb") as f:
                print("saving")
                result = blob_client.upload_blob(f, overwrite=True,
                                                 content_settings=ContentSettings(content_type='image/jpeg'))
                print(result)
        print("Uploading image done, sending event...")
        event_payload = {"blob_name": storage_info['blobName'], "device_key": device_key}
        await event_hub_helper.send_event(EVENT_HUB_NAME, event_payload)
        print("Successfully sent verification request,\n")
    except Exception as ex:
        print(type(ex))
        print(ex)
        print()
        return ex


########################################################
# Main IoT device function
########################################################
async def main():
    print("IoT device starting...")
    conn_str = os.getenv("DEVICE_CONN_STR")
    device_key = os.getenv("DEVICE_KEY")
    if conn_str is None or device_key is None:
        print("You need to export your device connection string and device key to env.")
        return
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    try:
        print("Connecting to the Azure IoT Hub...")
        await device_client.connect()
        print("Connected successfully. Listening messages from the cloud...")

        device_client.on_message_received = message_handler

        while True:
            img_path = input("\nPlease provide URL for an image\n")
            await trigger_verification_request(img_path, device_key, device_client)
            time.sleep(1)
    except ValueError as ex:
        print("[ERROR] ValueError occur: {}".format(ex))
    except azure.iot.device.exceptions.CredentialError as ex:
        print("[ERROR] {}".format(ex))
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Shutting down...")
        # time.sleep(1)
    except Exception as ex:
        print("[ERROR] {}".format(ex))
    finally:
        await device_client.shutdown()
        print("Device shut down successfully")


if __name__ == "__main__":
    # print("test")
    asyncio.run(main())
