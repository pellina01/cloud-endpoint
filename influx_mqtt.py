class listen():

    def on_message(self, client, userdata, msg):
        import json
        import paho.mqtt.client as mqtt

        recieved_list = json.loads(msg.payload.decode("utf-8"))
        data = []
        if recieved_list["status"] == "sending":
            print("recieved message from: %s =" %
                  self.topic + recieved_list["value"])

            data.append("{measurement},index={index} value={value} {timestamp}"
                        .format(measurement=self.topic, index=self.topic, value=recieved_list["value"], timestamp=recieved_list["time"]))

            self.influxClient.write_points(
                data, database='awsblog', time_precision='ms', batch_size=1, protocol='line')

        elif recieved_list["status"] == "connected":
            print("connected %s" % self.topic)

        elif recieved_list["status"] == "disconnected":
            print("disconnected %s" % self.topic)

    def __init__(self, topic, mqtturl, influxHost, database, influxPort=8086, mqttport=1883, ttl=60):
        import paho.mqtt.client as mqtt
        from influxdb import InfluxDBClient

        self.topic = topic
        self.mqtturl = mqtturl
        self.mqttport = mqttport
        self.ttl = ttl
        self.influxHost = influxHost
        self.influxPort = influxPort

        self.influxClient = InfluxDBClient(
            host=self.influxHost, port=self.influxPort)

        self.client = mqtt.Client()

        self.connected = False
        self.printed = False
        while self.connected is False:
            try:
                self.client.connect(self.mqtturl, self.mqttport, self.ttl)
                self.connected = True
            except:
                if not self.printed:
                    print(
                        "failed to establish connection with topic: %s,reconnecting..." % self.topic)
                    self.printed = True

        self.client.loop_start()

        self.client.subscribe(self.topic)

        self.client.message_callback_add(self.topic, self.on_message)

        print("Connected and subscribed to topic: " + self.topic)
