class handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient
        import logging
        import traceback

        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

        # self.database = database
        self.topic = topic
        self.status_checker = []
        if topic == "ph":
            self.unit = "pH"
        elif topic == "tb":
            self.unit = "NTU"
        elif topic == "temp":
            self.unit = "Celsius"
        else:
            self.unit = "No unit"

        self.value_serializer = self.json_serializer(self.topic, self.unit)
        self.status_serializer = self.json_serializer(
            "{}_status".format(self.topic), self.unit)

    def json_serializer(self, measurement, tag):
        def serialize(field):
            return [
                {
                    "measurement": measurement,
                    "tags": {
                        "unit": tag
                    },
                    "fields": {
                        "value": field
                    }
                }]
        return serialize

    def dbsend(self, recieved_list):
        try:
            json_body = []
            if recieved_list["status"] == "sending":
                json_body = self.value_serializer(recieved_list["value"])
                if len(self.status_checker) < 1:
                    json_body.append(self.status_serializer("connected"))
                    self.status_checker.append("placeholder")
                    print("connected %s" % self.topic)

            elif recieved_list["status"] == "connected":
                self.status_checker.append("placeholder")
                json_body = self.status_serializer("connected")
                print("connected %s" % self.topic)

            elif recieved_list["status"] == "disconnected":
                try:
                    self.status_checker.pop(0)
                    if len(self.status_checker) < 1:
                        json_body = self.status_serializer("disconnected")
                        print("disconnected %s" % self.topic)
                except:
                    pass

            try:
                self.influxClient.write_points(
                    json_body, time_precision='ms', protocol='json')
            except Exception as e:
                print("failed to write to influxdb: %s" % e)
                print(e)
                self.logging.error(self.traceback.format_exc())

        except Exception as e:
            print("failed to write to DB topic %s" % self.topic)
            print(e)
            self.logging.error(self.traceback.format_exc())

        finally:
            del json_body
