from influx_mqtt import listen
from config_cloud import config
import time

import logging
import traceback


error = config.error_file
url = config.url
ph = config.topic_ph
tb = config.topic_tb
temp = config.topic_temp
influxHost = config.influxHost
database = config.database
username = config.username
password = config.password


connected = False
while connected is False:
    try:
        logging.basicConfig(filename=error)
        ph = listen(ph, url, influxHost, database, username, password)
        tb = listen(tb, url, influxHost, database, username, password)
        temp = listen(temp, url, influxHost, database, username, password)
        connected = True
    except Exception as e:
        print("error occured: %s" % e)


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
