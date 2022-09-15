/*******************************************************************************
 * Copyright (c) 2022 amin TAYEBI
 *
 * Permission is hereby granted, free of charge, to anyone
 * obtaining a copy of this document and accompanying files,
 * to do whatever they want with them without any restriction,
 * including, but not limited to, copying, modification and redistribution.
 * NO WARRANTY OF ANY KIND IS PROVIDED.
 *
 * The script should be run on venv mode
 *******************************************************************************/


import context
import paho.mqtt.publish as publish

#deveui = ""
input1 = eval(input("for valve Arduino uno press (1), for valve Arduino nano press (2):"))

if (input1 == 1):
    deveui = "eui-70XXXX"
    print("deveui set to :  " + deveui)
elif (input1 == 2):
    deveui = "XXXXXXX"
    print("deveui set to :  " + deveui)



input2 = eval(input("If application ID is XXXXXXXXXX, press 1 otherwise please enter 2:"))
if (input2 == 1):
    appid = "XXXXXX"
    print("app id set to:  " + appid)
elif (input2 == 2):
    appid = input("please enter application ID:")
    print("app id set to:  " + appid)





publish.single("v3/" + appid + "@ttn/devices/" + deveui + "/down/push", \
               '{"downlinks":[{"f_port": 16,"frm_payload":"XXXX" ,"priority": "NORMAL"}]}', \
               hostname="eu1.cloud.thethings.network", \
               port=1883, auth={'username': "XXXXXXXXXXXX",
                                'password': "NNSXS.RXXXX"})

print("		is sent to the device " + deveui)


#print("v3/"+appid+"@ttn/devices/"+deveui+"/down/push", '{"downlinks":[{"f_port": 16,"frm_payload":"amin" ,"priority": "NORMAL"}]}',"eu1.cloud.thethings.network",1883, {'username':"XXXXXXXXXXX",  'password':"NNSXS.XXXXXX"})
# 00  AA==
# 01  AQ==
# 02  Ag==
# 03  Aw==
