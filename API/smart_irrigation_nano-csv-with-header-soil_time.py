#*******************************************************************************
# Copyright (c) 2022 amin TAYEBI
#
# Permission is hereby granted, free of charge, to anyone
# obtaining a copy of this document and accompanying files,
# to do whatever they want with them without any restriction,
# including, but not limited to, copying, modification and redistribution.
# NO WARRANTY OF ANY KIND IS PROVIDED.
#
# Setup invironment to run:
# The script should be run on venv mode in python3
# 
# Functionalities:
# - This mosule read sensor dragino LSE01 data and if "moisture is below 30%" open the Actuator (solenoid valve) for 2 seconds (defined on actuator downlink)
# - Reapeats forever
# - Works also with moisture value even 0  or 100 while previus versions just worked with moisture value 10-99
# - Save theese data to CSV file in currebt path: 
# i) soil humidity from Adafruite soil sensor 
# ii) date/time of data captured 
# *******************************************************************************/
#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re
import sys
from csv import writer
import csv

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/<app name>@ttn/devices/<sensor dev eui>/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = '<app name>'
password = 'NNSXS.XXX'



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


# create a csv file with header to write payloads to csv file online
file_name = open('sensor_payloads_nano.csv', 'a')
fields = []
fields.append('Payload')
fields.append('Payload_time')
writer_object = csv.DictWriter(file_name, fieldnames=fields)
writer_object.writeheader()
file_name.close()

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        # separate lines based on "uplink_message"

        try:

            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            line = msg.payload.decode()
            print(line)

            date2 = re.search('received_at":"(.*)Z"', line)
            t = date2.group(1)

            # find desired value between the json string
            payload = re.search('Moisture_percentage":(.*),"Valve', line)
            p = payload.group(1)

            # convert re.match to float
            #payload = float(payload.group(1))

            # convert float to int
            payloadi = int(p)

            # write payloads to csv file online
            # with open('sensor_payloads_nano.csv', 'a') as f:
            #     writer_object = writer(f)
            #     writer_object.writerow(payload2)
            file_name = open('sensor_payloads_nano.csv', 'a')
            fields = []
            fields.append('Payload')
            fields.append('Payload_time')

            writer_object = csv.DictWriter(file_name, fieldnames=fields)
            payload_data = [{'Payload': p, 'Payload_time': t}]
            writer_object.writerows(payload_data)
            file_name.close()

            if (payloadi < 70):
                    print(p , "%:   In Adafruite soil moisture is below 70% downlink sent to open the VALVE for 10 seconds")

                    # "Aw==" is euqal to 03 which defined on actuator if this downlink received open the valve for 10 seconds
                    publish.single("v3/<app name>@ttn/devices/<actuator dev eui>/down/push",
                           '{"downlinks":[{"f_port": 16,"frm_payload":"Aw==","priority": "NORMAL"}]}',
                           hostname="eu1.cloud.thethings.network", port=1883,
                           auth={'username': "<app name>",
                                 'password': "NNSXS.XXX"})


        except ValueError:
            print("That payload does not exist or is not in range")
        return None


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

