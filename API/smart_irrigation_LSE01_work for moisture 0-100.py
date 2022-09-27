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
# *******************************************************************************/
#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re

# Import writer class from csv module  or import csv
from csv import writer
import csv

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/<>app id@ttn/devices/<dev eui>/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = '<app-key>'
password = 'NNSXS.XXX'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    #client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        # separate lines based on "uplink_message"

        try:
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            line = msg.payload.decode()
            print(line)

        #find desired value between the json string
            payload = re.search('water_SOIL":"(.*) %', line)
            print(payload.group(1))

        #convert re.match to float
            payload = float(payload.group(1))

        #convert float to int
            payload2= int(payload)

            print(payload2)

        #Write each payload into csv file and append new value in new row lively
            # with open('sensor_payloads_LSE01.csv', 'a') as f:
            #  writer_object = writer(f)
            #  writer_object.writerow(payload2)

            if (payload2 < 30):
             print(payload2, "%:   moisture is below 30%")
            
        # "Ag==" is euqal to 02 which defined on actuator if this downlink received open the valve for 3 seconds
             publish.single("v3/<app id>@ttn/devices/<actuator dev eui->/down/push",
                           '{"downlinks":[{"f_port": 16,"frm_payload":"Ag==","priority": "NORMAL"}]}',
                           hostname="eu1.cloud.thethings.network", port=1883,
                           auth={'username': "<app id>",
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

