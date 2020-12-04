class handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient
        import logging
        import traceback

        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)

        self.logging = logging
        self.traceback = traceback
        self.logging.basicConfig(filename="error.log")

        self.database = database
        self.topic = topic

        if topic == "ph":
            self.unit = "pH"
        elif topic == "tb":
            self.unit = "NTU"
        elif topic == "temp":
            self.unit = "Celsius"
        else:
            self.unit = "No unit"

    def dbsend(self, recieved_list):
        try:
            self.data = []
            if recieved_list["status"] == "sending":
                print("saving message: %s" % recieved_list["value"])

                self.data.append("{measurement},unit={unit} value={value} {timestamp}"
                                 .format(measurement=self.topic, unit=self.unit, value=recieved_list["value"], timestamp=recieved_list["time"]))

            elif recieved_list["status"] == "connected":
                print("connected %s" % self.topic)

            elif recieved_list["status"] == "disconnected":
                print("disconnected %s" % self.topic)

            try:
                self.influxClient.write_points(
                    self.data, database=self.database, time_precision='ms', batch_size=1, protocol='line')
            except Exception as e:
                print("failed to write to influxdb: %s" % e)

        except Exception as e:
            print("failed to write to DB topic %s" % self.topic)
            print(e)
            self.logging.error(self.traceback.format_exc())

        finally:
            del self.data
