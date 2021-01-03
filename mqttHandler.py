class listen:

    def __message_callback_add(self, client, userdata, msg):
        try:
            self.influxHandler.dbsend(
                self.jsonParser(msg.payload.decode("utf-8")))
        except Exception as e:
            print("error occured: %s" % e)

    def __init__(self, topic, mqtturl, influxHost, database, username, password, influxPort=8086, mqttport=1883, keepalive=60):
        import paho.mqtt.client as mqtt
        from influxHandler import handler
        import json

        self.jsonParser = json.loads

        self.influxHandler = handler(
            influxHost, username, password, database, topic)

        mqttClient = mqtt.Client()

        connected = False
        printed = False
        while connected is False:
            try:
                mqttClient.connect(mqtturl, mqttport, keepalive)
                connected = True
            except:
                if not printed:
                    print(
                        "failed to establish connection with topic: %s, retryng.." % topic)
                    printed = True

        mqttClient.loop_start()

        mqttClient.subscribe(topic)

        mqttClient.message_callback_add(
            topic, self.__message_callback_add)

        print("Connected and subscribed to topic: %s" % topic)
