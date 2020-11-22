from config_cloud import config

import paho.mqtt.client as mqtt
import json

# This is the Subscriber

topic = config.topic
url = config.url


def on_connect(client, userdata, flags, rc):
    topic = "topic/ph"
    client.subscribe(topic)
    print("Connected with result code " +
          str(rc) + " subscribed to topic " + topic)


def on_message(client, userdata, msg):
    recieved_list = json.loads(msg.payload.decode("utf-8"))
    if recieved_list["status"] == "sending":
        print(recieved_list["message"])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

connected = False
printed = False
while connected is False:
    try:
        client.connect(url, 1883, 60)
        connected = True
    except:
        if not printed:
            print(
                "failed to establish connection with %s,reconnecting..." % url)
            printed = True


client.loop_forever()
