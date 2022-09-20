#!/usr/bin/env python3
import context
import paho.mqtt.subscribe as subscribe

import paho.mqtt.publish as publish
import json
import csv
import time

import re
import sys

# --------------------------------------------------------------subscribing function
message = subscribe.simple(topics=['#'], \
                           hostname="eu1.cloud.thethings.network", port=1883, \
                           auth={'username': "arduinosdi1222222222222222", \
                                 'password': "NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"},
                           msg_count=2)
# write output on 1.txt in the current path 
sys.stdout = open("1.txt", "w")

for a in message:
    print(a.payload)

# separate lines based on "uplink_message"
pattern = re.compile("uplink_message")

# create a csv file for sensor payload-output
sys.stdout = open("output.csv", "w")

# input file is 1.txt
for line in open("1.txt"):
    for match in re.finditer(pattern, line):

        # delete other chars before "Moisture_percentage"
        alist = line.split('Moisture_percentage":')

        # from the remain string, take the 2 first chars
        t = alist[-1][:2]
        t2 = t.replace('\n', '')
        print(t2)
        # convert string to int and do comparison
if (int(t2) < 90):publish.single("v3/arduinosdi1222222222222222@ttn/devices/eui-70b3d57ed0054220/down/push", '{"downlinks":[{"f_port": 16,"frm_payload":"Aw==","priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", port=1883, auth={'username': "arduinosdi1222222222222222", 'password': "NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})
