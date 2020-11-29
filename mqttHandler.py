class listen:

    def message_callback_add(self, client, userdata, msg):
        import json
        try:
            self.influxHandler.dbsend(json.loads(msg.payload.decode("utf-8")))
        except Exception as e:
            print("error occured: %" % e)

    def __init__(self, topic, mqtturl, influxHost, database, username, password, influxPort=8086, mqttport=1883, keepalive=60):
        import paho.mqtt.client as mqtt
        from influxHandler import handler

        self.influxHandler = handler(
            influxHost, username, password, database, topic)

        self.topic = topic
        self.mqttClient = mqtt.Client()

        self.connected = False
        self.printed = False
        while self.connected is False:
            try:
                self.mqttClient.connect(mqtturl, mqttport, keepalive)
                self.connected = True
            except:
                if not self.printed:
                    print(
                        "failed to establish connection with topic: %s, reconnecting..." % topic)
                    self.printed = True

        self.mqttClient.loop_start()

        self.mqttClient.subscribe(topic)

        self.mqttClient.message_callback_add(
            topic, self.message_callback_add)

        print("Connected and subscribed to topic: %s" % topic)

        del self.connected
        del self.printed
