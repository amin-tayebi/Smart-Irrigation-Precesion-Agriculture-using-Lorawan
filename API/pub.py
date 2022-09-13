import context
import paho.mqtt.publish as publish

publish.single("v3/<application name in TTN console>@ttn/devices/<Device EUI>/down/push", \
'{"downlinks":[{"f_port": 15,"frm_payload":"vu8=","priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", \
port=1883, auth={'username':"application name in TTN console",\
'password':"api password in TTN console"})

