#!/bin/zsh

echo "exporting connection string and device key to OS env variables"

# export connection string and device key to OS variables
export DEVICE_CONN_STR="HostName=cs5412-final-project-iothub-standard.azure-devices.net;DeviceId=phillips-hall-219;SharedAccessKey=PFudmC3zDRY2w4NhnDnYs+LVizbw94Ut8oJR0cUgmEo="
export DEVICE_KEY="PFudmC3zDRY2w4NhnDnYs+LVizbw94Ut8oJR0cUgmEo="

# print for double-check
echo "exported connection string: "
echo $DEVICE_CONN_STR
echo "exported device key: "
echo $DEVICE_KEY

echo "exported connection string and device key of Phillips-hall-219"
echo "running Python script"

# run python program
python ./device_script.py
