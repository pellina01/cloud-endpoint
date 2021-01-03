class serializer:
    def __init__(self, topic, unit):
        self.topic = topic
        self.unit = unit
        self.state = {
        "connected":self.connected,
        "disconnected":self.disconnected,
        "sending":self.sending
        }

    def serialize(self, recieved_list):
        return self.state.get(recieved_list["status"])(recieved_list)

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
        return self.influx_serializer(self.topic, self.unit, float(recieved_list["value"]))

    def connected(self, recieved_list):
        return self.influx_serializer("{}_status".format(self.topic), self.unit, "connected")

    def disconnected(self, recieved_list):
        return self.influx_serializer("{}_status".format(self.topic), self.unit, "disconnected")
