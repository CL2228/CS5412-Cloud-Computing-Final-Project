#!/bin/zsh

echo "exporting connection string and device key to OS env variables"

# export connection string and device key to OS variables
export DEVICE_CONN_STR="HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=phillips-hall-403;SharedAccessKey=SQQj1QJuvIgYdAoDV4gimZMf0OeaZUW7tBL/D21XIcM="
export DEVICE_KEY="SQQj1QJuvIgYdAoDV4gimZMf0OeaZUW7tBL/D21XIcM="

# print for double-check
echo "exported connection string: "
echo $DEVICE_CONN_STR
echo "exported device key: "
echo $DEVICE_KEY

echo "exported connection string and device key of Phillips-hall-403"
echo "running Python script"

# run python program
python ./device_script.py
