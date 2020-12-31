class serializer:
    def __init__(self, topic, unit):
        self.topic = topic
        self.unit = unit

    def serialize(self, recieved_list):
        return getattr(serializer, recieved_list["status"])(self, recieved_list)

    def influx_serializer(self, measurement, tag, field):
        return [{
            "measurement": measurement,
            "tags": {
                "unit": tag
            },
            "fields":   {
                "value": field
            }
        }]

    def sending(self, recieved_list):
        float(recieved_list["value"])
        return self.influx_serializer(self.topic, self.unit, recieved_list["value"])

    def connected(self, recieved_list):
        return self.influx_serializer("{}_status".format(self.topic), self.unit, "connected")

    def disconnected(self, recieved_list):
        return self.influx_serializer("{}_status".format(self.topic), self.unit, "disconnected")
