from subscribe_cloud import listen
import time

ph = listen("topic/ph", "")
tb = listen("topic/tb", "")
while True:
    print(ph.on_message())
    time.sleep(1)
