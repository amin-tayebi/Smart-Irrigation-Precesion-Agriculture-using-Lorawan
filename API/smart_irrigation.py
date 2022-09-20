# This module: 1- subscribe to the application in TTN (any lorawan server) to read payloads of nano-IoT33 measures
#              2- Speparate the moisture sensor payloads
#              3- Process each 2 message (as msg_count is 2) if it is less than 70% or not
#              4- If below 70% then Publish downlink to the application in TTN (any lorawan server) to TURN ON solenoid Valve for 10 seconds (possible to be modified in arduino code)
/*******************************************************************************
 * Copyright (c) 2022 amin TAYEBI
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * The script should be run on venv mode in python3
 *******************************************************************************/
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
                           auth={'username': "app name", \
                                 'password': "NNSXS.XXX"},
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
if (int(t2) < 90):publish.single("v3/<app name>@ttn/devices/<dev eui>/down/push", '{"downlinks":[{"f_port": 16,"frm_payload":"Aw==","priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", port=1883, auth={'username': "<app name>", 'password': "NNSXS.XXX"})
  # Aw== is 03 which open valve for 10 seconds
