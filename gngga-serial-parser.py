import json

import serial
import pynmea2
import paho.mqtt.client as mqtt

ser = serial.Serial('/dev/ttyUSB0')
msg_list=[]


def my_func(client, userdata, flags, rc):
    print("Connection established!")

client = mqtt.Client()
client.on_connect = my_func
client.tls_set()
client.username_pw_set(username='upbdrive', password='upbdriveilabs')
client.connect("ihoria.tech", 8883)
client.loop_start()

while True:
    lonlat = []
    line = ser.readline()
    line = line.decode().strip()
    if line.startswith('$GNGGA'):
        msg = pynmea2.parse(line)
        data = {'lat':msg.latitude, 'lon':msg.longitude}
        rc = client.publish("gps", json.dumps(data))