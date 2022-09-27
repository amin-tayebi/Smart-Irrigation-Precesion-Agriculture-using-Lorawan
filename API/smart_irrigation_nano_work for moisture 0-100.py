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
# - This mosule read sensor dragino LSE01 data and if "moisture is below 70%" open the Actuator (solenoid valve) for 10 seconds (defined on actuator downlink)
# - Reapeats forever
# - Works also with moisture value even 0 or 100 while previus versions just worked with moisture value 10-99
# *******************************************************************************/
#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re
import sys
from csv import writer

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/<app id>@ttn/devices/<dev id>/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = '<app id>'
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):

        # separate lines based on "uplink_message"

        try:
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            line = msg.payload.decode()
            print(line)

            # find desired value between the json string
            payload = re.search('Moisture_percentage":(.*),"Valve', line)
            print(payload.group(1))

            # convert re.match to float
            payload = float(payload.group(1))

            # convert float to int
            payload2 = int(payload)

            print(payload2)# convert string to int and do comparison
            # with open('sensor_payloads_nano.csv', 'a') as f:
            #         writer_object = writer(f)
            #         writer_object.writerow(payload2)

            if (payload2 < 70):
                    print(payload2 , "%:   moisture is below 70%")
                    publish.single("v3/<app id>@ttn/devices/<actuator dev eui>/down/push",
                           '{"downlinks":[{"f_port": 16,"frm_payload":"Aw==","priority": "NORMAL"}]}',
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

