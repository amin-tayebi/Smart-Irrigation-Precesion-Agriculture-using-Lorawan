#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re
import sys

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/app-3@ttn/devices/eui-a840419e918220ed-lse01/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'app-3'
password = 'NNSXS.MVFULYOGEG4B5XBPRN4WHC2QHRF2IPSBDAQ7PVA.TF65V52GWNEIE7WAGQX6RHIK6RDVDBN3UXONDZKTN6DWYE4L2PAQ'

# write output on 1.txt in the current path
#sys.stdout = open("output.csv", "w")

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
         alist = line.split('water_SOIL":"0.')

        # from the remain string, take the 2 first chars
         t = alist[-1][:2]
        #t2 = t.replace('\n', '')
        #print(t2)
        # convert string to int and do comparison
         if (int(t) < 40):
            #print(t , "moisture is below 60%")
            publish.single("v3/arduinosdi1222222222222222@ttn/devices/eui-70b3d57ed0054220/down/push",
                           '{"downlinks":[{"f_port": 17,"frm_payload":"Aw==","priority": "NORMAL"}]}',
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

