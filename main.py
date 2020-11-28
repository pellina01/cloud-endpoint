from subscribe_cloud import listen
from config_cloud import config
import time

import logging
import traceback


error = config.error_file
url = config.url
ph = config.topic_ph
tb = config.topic_tb
temp = config.topic_temp


logging.basicConfig(filename=error)
ph = listen(ph, url)
tb = listen(tb, url)
temp = listen(temp, url)

while True:
    try:
        print("listening..")
        time.sleep(10)
    except Exception as e:
        print("error occured: " + traceback.format_exc())
        print("error message: " + e)
        logging.error(traceback.format_exc())
        time.sleep(2)
