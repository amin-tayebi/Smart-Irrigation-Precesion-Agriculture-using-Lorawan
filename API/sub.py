import context 
import paho.mqtt.subscribe as subscribe

message = subscribe.simple(topics=['#'], \
hostname="eu1.cloud.thethings.network", port=1883, \
auth={'username':"application name",'password':"NNSXS.xxxx"}, msg_count=10)
for a in message:
    print(a.topic)
    print(a.payload)
    #print(a.payload)


