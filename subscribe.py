import paho.mqtt.client as mqtt

# This is the Subscriber


def on_connect(client, userdata, flags, rc):
    topic = "topic/ph"
    client.subscribe(topic)
    print("Connected with result code " +
          str(rc) + " subscribed to topic " + topic)


def on_message(client, userdata, msg):
    print(msg.payload.decode())
    # if msg.payload.decode() == "Hello world!":
    #     print("Yes!")
    #     client.disconnect()


client = mqtt.Client()
client.connect("127.0.0.0", 1883, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
