import context
import paho.mqtt.publish as publish


#valve = input("Please enter VALVE mode: ")
deveui = input("Please enter DEVICE ID:")
appid = input("Please enter application ID:")



publish.single("v3/"+appid+"@ttn/devices/"+deveui+"/down/push", \
'{"downlinks":[{"f_port": 16,"frm_payload":"amin" ,"priority": "NORMAL"}]}', hostname="eu1.cloud.thethings.network", \
port=1883, auth={'username':"arduinosdi1222222222222222",\
'password':"NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})


print("		is sent to the device "+ deveui)
# DEV EUI:
#nanoiot33eui-70b3d57ed005529e
#eui-70b3d57ed0054220

#app ID
#arduinosdi1222222222222222



#print("v3/"+appid+"@ttn/devices/"+deveui+"/down/push", \
#'{"downlinks":[{"f_port": 16,"frm_payload":"02" ,"priority": "NORMAL"}]}',"eu1.cloud.thethings.network", \
#1883, {'username':"arduinosdi1222222222222222",\
#'password':"NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})
