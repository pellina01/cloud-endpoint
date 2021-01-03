class serializer:
    def __init__(self, topic, unit):
        self.topic = topic
        self.unit = unit
        self.state = {
        "connected":self.__connected,
        "disconnected":self.__disconnected,
        "sending":self.__sending
        }

    def serialize(self, recieved_list):
        return self.state.get(recieved_list["status"])(recieved_list)

    def __influx_serializer(self, measurement, tag, field):
        return [{
            "measurement": measurement,
            "tags": {
                "unit": tag
            },
            "fields":   {
                "value": field
            }
        }]

    def __sending(self, recieved_list):
        return self.__influx_serializer(self.topic, self.unit, float(recieved_list["value"]))

    def __connected(self, recieved_list):
        return self.__influx_serializer("{}_status".format(self.topic), self.unit, "connected")

    def __disconnected(self, recieved_list):
        return self.__influx_serializer("{}_status".format(self.topic), self.unit, "disconnected")
