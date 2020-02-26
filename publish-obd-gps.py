import json

import serial
import pynmea2
import paho.mqtt.client as mqtt
import obd
from time import sleep

ser = serial.Serial('/dev/ttyUSB1')
msg_list=[]


def my_func(client, userdata, flags, rc):
    print("Sent data to broker.")

client = mqtt.Client()
client.on_publish = my_func
client.tls_set()
client.username_pw_set(username='upbdrive', password='upbdriveilabs')
client.connect("ihoria.tech", 8883)
client.loop_start()

sensors = ["ENGINE_LOAD","COOLANT_TEMP","INTAKE_PRESSURE","RPM","SPEED","INTAKE_TEMP","MAF","THROTTLE_POS","FUEL_LEVEL"]

connection = obd.Async("/dev/ttyUSB0")

for sensor in sensors:
    connection.watch(obd.commands[sensor])

connection.start()

while True:
    data = {}
    response = connection.query(obd.commands["RPM"])

    for sensor in sensors:
        response = connection.query(obd.commands[sensor])
        if response.is_null():
            continue
        
        val = {'val':response.value.magnitude, 'unit':response.unit}
        data[sensor] = val
    
    # GPS
    line = ser.readline()
    line = line.decode().strip()
    if line.startswith('$GNGGA'):
        msg = pynmea2.parse(line)
        lon = {'val':msg.longitude, 'unit':'degrees'}
        lat = {'val':msg.latitude, 'unit':'degrees'}
        data['LON'] = lon
        data['LAT'] = lat

        client.publish("gps", json.dumps(data))
