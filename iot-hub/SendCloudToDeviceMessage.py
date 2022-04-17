import random
import sys
from azure.iot.hub import IoTHubRegistryManager
import json

MESSAGE_COUNT = 2
AVG_WIND_SPEED = 10.0
MSG_TXT = "{\"service client sent a message\": %.2f}"

CONNECTION_STRING = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=doIck9pzBpEM9/Fs+oF9xbtWhPJFzMBMzRLZ+tlfKgk="
DEVICE_ID = "test-device"


def iothub_messaging_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        # for i in range(0, MESSAGE_COUNT):
        #     print('Sending message: {0}'.format(i))
        #     data = MSG_TXT % (AVG_WIND_SPEED + (random.random() * 4 + 2))
        #
        #     props = {}
        #     # optional: assign system properties
        #     props.update(messageId="message_%d" % i)
        #     props.update(correlationId="correlation_%d" % i)
        #     props.update(contentType="application/json")
        #
        #     # optional: assign application properties
        #     prop_text = "PropMsg_%d" % i
        #     props.update(testProperty=prop_text)
        #
        #     registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)

        props = {}
        props.update(contentType="application/json")
        print(props)
        payload = {"name": "cl2228"}
        payload = json.dumps(payload)
        registry_manager.send_c2d_message(DEVICE_ID, payload, props)

        try:
            input("Press Enter to continue...\n")
        except:
            pass
    # except Exception as ex:
    #
    #     print("Unexpected error {}" .format(str(ex)))
    #     print(type(ex))
    #     return
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging service sample stopped")


if __name__ == '__main__':
    print("Starting the Python IoT Hub C2D Messaging service sample...")

    iothub_messaging_sample_run()
