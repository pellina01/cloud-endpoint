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

        self.topic = topic
        self.status_checker = []

        switch = {
            "ph": "pH",
            "tb": "NTU",
            "temp": "Celsius"
        }
        self.unit = switch.get(topic, "No unit")
        del switch

        self.value_serializer = self.json_serializer(self.topic, self.unit)
        self.status_serializer = self.json_serializer(
            "{}_status".format(self.topic), self.unit)

    def json_serializer(self, measurement, tag):
        def serialize(field):
            return {
                "measurement": measurement,
                "tags": {
                    "unit": tag
                },
                "fields":   {
                    "value": field
                }
            }
        return serialize

    def dbsend(self, recieved_list):
        try:
            self.influxClient.write_points(
                getattr(handler, recieved_list["status"])(
                    self, [], recieved_list["value"]),
                time_precision='ms', protocol='json')
# second parameter of getattr must always be empty list since the function needs an empty lists
        except Exception as e:
            print("failed to write to DB topic %s" % self.topic)
            print(e)
            self.logging.error(self.traceback.format_exc())

    def sending(self, *args):
        args[0].append(self.value_serializer(args[1]))
        if len(self.status_checker) < 1:
            args[0].append(self.status_serializer("connected"))
            self.status_checker.append("placeholder")
            print("connected %s" % self.topic)
        return args[0]

    def connected(self, *args):
        self.status_checker.append("placeholder")
        if len(self.status_checker) == 1:
            args[0].append(self.status_serializer("connected"))
            print("connected %s" % self.topic)
        return args[0]

    def disconnected(self, *args):
        try:
            self.status_checker.pop(0)
        except:
            pass
        if len(self.status_checker) < 1:
            args[0].append(self.status_serializer("disconnected"))
            print("disconnected %s" % self.topic)
        return args[0]
