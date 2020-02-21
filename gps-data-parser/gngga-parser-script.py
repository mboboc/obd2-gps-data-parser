import json
import time
import serial
import pynmea2
import paho.mqtt.client as mqtt

msg_list = []
lonlat = []
f = open("../gps-data-dump.ubx", "rb")
w = open("../data.txt", "w")

ser = serial.Serial('/dev/ttyUSB0')


def my_func(client, userdata, flags, rc):
    print("Sent data to Horia.")


client = mqtt.Client()
client.on_publish = my_func
client.tls_set()
client.username_pw_set(username='upbdrive', password='upbdriveilabs')
client.connect("ihoria.tech", 8883)
client.loop_start()

while True:
    f.seek(0)
    for e in f:
        try:
            line = e.decode().strip()
        except UnicodeError:
            continue

        if line.startswith('$GNGGA'):
            star = line.index('*')
            line = line[:star]
            msg = pynmea2.parse(line)
            data = {'lat': msg.latitude, 'lon': msg.longitude}
            client.publish("gps", json.dumps(data))
            time.sleep(1)

# print(f'Timestamp: {msg.timestamp}')
# print(f'Latitude: {msg.latitude}')
# print(f'Longitute: {msg.longitude}')
# print(f'Latitude direction: {msg.lat_dir}')
# print(f'Longitude direction: {msg.lon_dir}')
# print(f'GPS quality indicator: {msg.gps_qual}')
# print(f'Satellites used: {msg.num_sats}')
# print('Longitude {}'.format(msg.lon))
# print('Longitude {}'.format(msg.lat))
#
# print(f'Horizontal dilution of precision: {msg.horizontal_dil}')
# print(f'Mean sea level altitude: {msg.altitude}')
# print(f'Altitude unit: {msg.altitude_units}')
#
# print(f' Geoidal separation: {msg.geo_sep}')
# print(f' Geoidal separation unit: {msg.geo_sep_units}')
# print(f' Age GPS data: {msg.age_gps_data}')
# print(f' Differential reference station ID: {msg.ref_station_id}')
