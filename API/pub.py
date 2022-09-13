import context
import paho.mqtt.publish as publish

#publish.single("v3/arduinosdi1222222222222222/devices/nanoiot33eui-70b3d57ed005529e/down/push", '{"downlinks":[{"f_port": 2,"frm_payload":"02","priority": "HIGHEST"}]}', hostname="eu1.cloud.thethings.network", port=1883, auth={'username':"arduinosdi1222222222222222",'password':"NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})
publish.single("v3/arduinosdi1222222222222222@ttn/devices/eui-70b3d57ed0054220/down/push", \
'{"downlinks":[{"f_port": 15,"frm_payload":"vu8=","priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", \
port=1883, auth={'username':"arduinosdi1222222222222222",\
'password':"NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})
#nanoiot33eui-70b3d57ed005529e
#eui-70b3d57ed0054220
