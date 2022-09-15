import context
import paho.mqtt.publish as publish

#deveui = ""
input1 = eval(input("for valve Arduino uno press (1), for valve Arduino nano press (2):"))

if (input1 == 1):
    deveui = "eui-70b3d57ed0054220"
    print("deveui set to :  " + deveui)
elif (input1 == 2):
    deveui = "nanoiot33eui-70b3d57ed005529e"
    print("deveui set to :  " + deveui)



input2 = eval(input("If application ID is aroduinosdi1222222222222222, press 1 otherwise please enter 2:"))
if (input2 == 1):
    appid = "arduinosdi1222222222222222"
    print("app id set to:  " + appid)
elif (input2 == 2):
    appid = input("please enter application ID:")
    print("app id set to:  " + appid)





publish.single("v3/" + appid + "@ttn/devices/" + deveui + "/down/push", \
               '{"downlinks":[{"f_port": 16,"frm_payload":"amin" ,"priority": "NORMAL"}]}', \
               hostname="eu1.cloud.thethings.network", \
               port=1883, auth={'username': "arduinosdi1222222222222222",
                                'password': "NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})

print("		is sent to the device " + deveui)


#print("v3/"+appid+"@ttn/devices/"+deveui+"/down/push", '{"downlinks":[{"f_port": 16,"frm_payload":"amin" ,"priority": "NORMAL"}]}',"eu1.cloud.thethings.network",1883, {'username':"arduinosdi1222222222222222",  'password':"NNSXS.RDHIBKJLMCRK2TQOVZMB35HYHIZZHRLNUBU3FRA.US4FXZIZW7DGKFWCZOKPX7BKGMG4TESJXN26OJPP5BPMO3PFVZCA"})
# 00  AA==
# 01  AQ==
# 02  Ag==
# 03  Aw==
