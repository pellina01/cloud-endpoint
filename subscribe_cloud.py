class listen():

    def on_message(self, client, userdata, msg):
        import json
        self.recieved_list = json.loads(self.msg.payload.decode("utf-8"))
        if self.recieved_list["status"] == "sending":
            print(recieved_list["message"])
        elif self.recieved_list["status"] == "connected":
            print("connected %s" % self.topic)
        elif self.recieved_list["status"] == "disconnected":
            print("disconnected %s" % self.topic)

    def __init__(self, topic, url, port=1883, ttl=60):
        import paho.mqtt.client as mqtt

        self.topic = topic
        self.url = url
        self.port = port
        self.ttl = ttl

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connected = False
        self.printed = False
        while self.connected is False:
            try:
                self.client.connect(self.url, self.port, self.ttl)
                self.connected = True
            except:
                if not self.printed:
                    print(
                        "failed to establish connection with topic: %s,reconnecting..." % self.topic)
                    self.printed = True

        self.client.loop_start()

        client.subscribe(self.topic)
        print("Connected with result code " +
              str(self.rc) + " subscribed to topic: " + self.topic)
