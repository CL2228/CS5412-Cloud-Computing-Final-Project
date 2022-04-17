import json
import time
from azure.iot.device import IoTHubDeviceClient

RECEIVED_MESSAGES = 0

CONNECTION_STRING = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=test-device;SharedAccessKey=Fj13ZONv0svBqCmqk7BG29Aqd1tF/7P5983RJLbF6zk="

GATES_STR = "HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=gates-hall-g01;SharedAccessKey=ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="

def message_handler(message):
    global RECEIVED_MESSAGES
    RECEIVED_MESSAGES += 1
    print("")
    print("Message received:")

    for prop in vars(message).items():
        print("    {}".format(prop))
    print("-----")
    data = vars(message)['data']
    data = json.loads(data)
    print(type(data))
    print(data)

    print("Total calls received: {}".format(RECEIVED_MESSAGES))


def main():
    print("Starting the Python IoT Hub C2D Messaging device sample...")

    client = IoTHubDeviceClient.create_from_connection_string(GATES_STR)

    print("Waiting for C2D messages, press Ctrl-C to exit")
    try:
        # Attach the handler to the client
        client.on_message_received = message_handler

        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()


if __name__ == "__main__":
    main()
