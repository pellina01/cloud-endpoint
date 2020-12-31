class handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient
        import logging
        import traceback
        from serializer import serializer
        from status_checker import status_checker

        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)
        self.influxClient.switch_database(database)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")
        self.topic = topic
        switch = {
            "ph": "pH",
            "tb": "NTU",
            "temp": "Celsius",
            "do": "mg/L"
        }

        self.serializer = serializer(topic, switch.get(topic, "No unit"))
        self.checker = status_checker()

    def dbsend(self, recieved_list):
        try:
            if self.checker.isValid(recieved_list):
                self.influxClient.write_points(
                    self.serializer.serialize(recieved_list),
                    time_precision='ms', protocol='json')
        except Exception as e:
            print("failed to write to DB topic %s" % self.topic)
            print(self.traceback.format_exc())
            self.logging.error(self.traceback.format_exc())
