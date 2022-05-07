#!/bin/zsh

echo "exporting connection string and device key to OS env variables"

# export connection string and device key to OS variables
export DEVICE_CONN_STR="HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=gates-hall-g01;SharedAccessKey=ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="
export DEVICE_KEY="ETLt4rqzS+1Fo1tOfzq+sKfMoPaG1c8sI9+9UmW6QT4="

# print for double-check
echo "exported connection string: "
echo $DEVICE_CONN_STR
echo "exported device key: "
echo $DEVICE_KEY

echo "exported connection string and device key of Gates-hall-g01."
echo "running Python script"

# run python program
python ./device_script.py
