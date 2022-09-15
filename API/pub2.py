import context
import paho.mqtt.publish as publish


#valve = input("Please enter VALVE mode: ")
deveui = input("Please enter DEVICE ID:")
appid = input("Please enter application ID:")



publish.single("v3/"+appid+"@ttn/devices/"+deveui+"/down/push", \
'{"downlinks":[{"f_port": 16,"frm_payload":"xxxx" ,"priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", \
port=1883, auth={'username':"app1",\
'password':"NNSXS.xxx"})


print("		is sent to the device "+ deveui)
