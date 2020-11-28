from influx_mqtt import listen
from config_cloud import config
import time

import logging
import traceback
import configparser


config.read('config.ini')

error = config['cloud']['error_file']
url = config['cloud']['url']
ph = config['cloud']['topic_ph']
tb = config['cloud']['topic_tb']
temp = config['cloud']['topic_temp']
influxHost = config['cloud']['influxHost']
database = config['cloud']['database']
username = config['cloud']['username']
password = config['cloud']['password']


logging.basicConfig(filename=error)
ph = listen(ph, url, influxHost, database, username, password)
tb = listen(tb, url, influxHost, database, username, password)
temp = listen(temp, url, influxHost, database, username, password)
connected = True


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
