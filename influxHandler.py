class handler:
    def __init__(self, influxHost, username, password, database, topic, influxPort=8086):
        from influxdb import InfluxDBClient

        self.influxClient = InfluxDBClient(
            influxHost, influxPort, username, password)

        self.database = database
        self.topic = topic

        if topic == "ph":
            self.unit = "pH"
            print(self.unit)
        elif topic == "tb":
            self.unit = "NTU"
            print(self.unit)
        elif topic == "temp":
            self.unit = "Celsius"
            print(self.unit)
        else:
            self.unit = "No unit"

        print("finished influx setup")

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
                    self.data, database=self.database, protocol='line')
            except Exception as e:
                print("failed to write to influxdb: %s" % e)

        except Exception as e:
            print("failed to write to DB topic %s" % self.topic)
            print(e)

        finally:
            del self.data
