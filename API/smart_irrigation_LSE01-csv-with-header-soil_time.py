#!/usr/bin/env python3
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
import re
from csv import writer
import csv

broker = 'eu1.cloud.thethings.network'
port = 1883
topic = "v3/app-3@ttn/devices/eui-a840419e918220ed-lse01/up"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'app-3'
password = 'NNSXS.MVFULYOGEG4B5XBPRN4WHC2QHRF2IPSBDAQ7PVA.TF65V52GWNEIE7WAGQX6RHIK6RDVDBN3UXONDZKTN6DWYE4L2PAQ'



def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    # client.on_connect = on_connect
    client.connect(broker, port)
    return client


file_name = open('new_file.csv', 'a')
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
            payload = re.search('water_SOIL":"(.*) %', line)
            p = payload.group(1)
            print(p)



            # convert re.match to float
            payload = float(payload.group(1))

            # convert float to int
            payload2 = int(payload)

            print(payload2)

            file_name = open('new_file.csv', 'a')
            fields = []
            fields.append('Payload')
            fields.append('Payload_time')
            writer_object = csv.DictWriter(file_name, fieldnames=fields)
            payload_data = [{'Payload': p, 'Payload_time': t}]
            writer_object.writerows(payload_data)
            file_name.close()


            if (payload2 < 30):
                print(payload2, "%:   In LSE01 sensor moisture is below 30%")

                # "Ag==" is euqal to 02 which defined on actuator if this downlink received open the valve for 3 seconds
                publish.single("v3/arduinosdi1222222222222222@ttn/devices/eui-70b3d57ed0054220/down/push",
                               '{"downlinks":[{"f_port": 16,"frm_payload":"Ag==","priority": "NORMAL"}]}',
                               hostname="eu1.cloud.thethings.network", port=1883,
                               auth={'username': "arduinosdi1222222222222222",
                                     'password': "NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})


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

