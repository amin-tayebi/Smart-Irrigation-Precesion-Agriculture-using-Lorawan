#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re
import sys

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/arduinosdi1222222222222222@ttn/devices/nanoiot33eui-70b3d57ed005529e/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'arduinosdi1222222222222222'
password = 'NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA'

# write output on 1.txt in the current path
#sys.stdout = open("1.txt", "w")

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

        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        line = msg.payload.decode()
        # separate lines based on "uplink_message"

        pattern = re.compile("uplink_message")
        for match in re.finditer(pattern, line):

        # delete other chars before "Moisture_percentage"
         alist = line.split('Moisture_percentage":')

        # from the remain string, take the 2 first chars
         t = alist[-1][:2]
        #t2 = t.replace('\n', '')
        #print(t2)
        # convert string to int and do comparison
         if (int(t) < 90):
            print(t , "moisture is below 70%")
            publish.single("v3/arduinosdi1222222222222222@ttn/devices/eui-70b3d57ed0054220/down/push",
                           '{"downlinks":[{"f_port": 16,"frm_payload":"Aw==","priority": "NORMAL"}]}',
                           hostname="eu1.cloud.thethings.network", port=1883,
                           auth={'username': "arduinosdi1222222222222222",
                                 'password': "NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})


    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

