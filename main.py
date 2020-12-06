from mqttHandler import listen
import time
import json
import logging
import traceback

# json_file = open('config.json')
# data = json.load(json_file)
# json_file.close()

with open('config.json', 'r') as file:
    data = json.loads(file.read())

cloud = {}
for key, value in data["cloud"].items():
    cloud.update({key: value})


logging.basicConfig(filename=cloud["error_file"])

topics = [cloud["ph_topic"], cloud["tb_topic"], cloud["temp_topic"]]

sensors = []
for topic in topics:
    sensors.append(listen(topic, cloud["url"], cloud["influxHost"],
                          cloud["database"], cloud["username"], cloud["password"]))


listening = True
while True:
    try:
        if listening is True:
            print("listening..")
            listening = False
    except Exception as e:
        print("error occured: %s" % traceback.format_exc())
        print("error message: %s" % e)
        logging.error(traceback.format_exc())
        listening = True
        time.sleep(2)
