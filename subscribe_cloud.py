import paho.mqtt.client as mqtt
import json

# This is the Subscriber

topic = "topic/ph"
url = "ec2-18-206-177-119.compute-1.amazonaws.com"


def on_connect(client, userdata, flags, rc):
    topic = "topic/ph"
    client.subscribe(topic)
    print("Connected with result code " +
          str(rc) + " subscribed to topic " + topic)


def on_message(client, userdata, msg):
    recieved_list = json.loads(msg.payload.decode("utf8"))
    print(recieved_list["message"])
    if msg.payload.decode() == "Hello world!":
        print("Yes!")


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
