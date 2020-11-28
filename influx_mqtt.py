class listen:

    def message_callback_add(self, client, userdata, msg):
        import json

        try:
            recieved_list = json.loads(msg.payload.decode("utf-8"))
            self.data = []
            if recieved_list["status"] == "sending":
                print("recieved message from: %s =" %
                      self.topic + recieved_list["value"])

                self.data.append("{measurement},topic={topic} value={value} {timestamp}"
                                 .format(measurement=self.topic, topic=self.topic, value=recieved_list["value"], timestamp=recieved_list["time"]))

                try:
                    self.influxClient.write_points(
                        self.data, database=self.database, protocol='line')
                except Exception as e:
                    print("failed to write to influxdb: %s" % e)

            elif recieved_list["status"] == "connected":
                print("connected %s" % self.topic)

            elif recieved_list["status"] == "disconnected":
                print("disconnected %s" % self.topic)

        except Exception as e:
            print("error occured: %s " % e)
            print("recieved value: %s" % msg.payload.decode("utf-8"))

    def __init__(self, topic, mqtturl, influxHost, database, username, password, influxPort=8086, mqttport=1883, keepalive=60):
        import paho.mqtt.client as mqtt
        from influxdb import InfluxDBClient

        self.topic = topic
        self.database = database

        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)

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
