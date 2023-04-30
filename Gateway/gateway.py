import paho.mqtt.client as mqtt
import time
import sys
import random
from uart import *

KEY = "6NvUzxxLlj8y36QOKtox7e71lJHx_oia"
MQTT_SERVER = "io.adafruit.com"
MQTT_PORT = 1883
MQTT_USERNAME = "ltduc147"
MQTT_PASSWORD = "6NvUzxxLlj8y36QOKtox7e71lJHx_oia"[::-1]
MQTT_TOPIC = ["ltduc147/feeds/pump-switch", "ltduc147/feeds/auto", "ltduc147/feeds/semi-auto"]
MQTT_TOPIC_PUB_NAME = "SmartBin2907123/feeds/V17"
MQTT_TOPIC_PUB_INDEX = "SmartBin2907123/feeds/V16"

def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    for topic in MQTT_TOPIC:
        client.subscribe(topic)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")
    
def mqtt_disconnected(client):
    print("Disconnected ... ")
    sys.exit(1)

def mqtt_message(client, userdata, msg):
    # Run when Receive message from server
    print("Receive data: " + msg.payload.decode()  + ", feed id: ", msg.topic)
    # write received msg to hardware
    writeCmd(msg.payload.decode(),msg.topic)
    


        
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_message = mqtt_message
mqttClient.on_disconnect = mqtt_disconnected
mqttClient.on_subscribe = mqtt_subscribed

mqttClient.loop_start()



while True:
    readSerial(mqttClient)
    time.sleep(1)
    pass