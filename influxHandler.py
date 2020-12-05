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
        self.status_checker = 0

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
            json_body = []
            if recieved_list["status"] == "sending":
                json_body = [
                    {
                        "measurement": self.topic,
                        "tags": {
                            "unit": self.unit
                        },
                        # "time": recieved_list["time"],
                        "fields": {
                            "value": recieved_list["value"]
                        }
                    }]

            elif recieved_list["status"] == "connected":
                self.status_checker += 1
                json_body = [
                    {
                        "measurement": "{} status".format(self.topic),
                        "tags": {
                            "unit": self.unit
                        },
                        "fields": {
                            "status": "connected",
                            "value": "1"
                        }
                    }]
                print("connected %s" % self.topic)

            elif recieved_list["status"] == "disconnected":
                self.status_checker -= 1 if self.status_checker > 0 else 0
                if self.status_checker == 0:
                    json_body = [
                        {
                            "measurement": "{} status".format(self.topic),
                            "tags": {
                                "unit": self.unit
                            },
                            "fields": {
                                "status": "disconnected",
                                "value": "0"
                            }
                        }]
                    print("disconnected %s" % self.topic)

            try:
                # self.influxClient.write_points(
                #     self.data, database=self.database, time_precision='ms', batch_size=1, protocol='line')
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
            # del self.data
            del json_body
