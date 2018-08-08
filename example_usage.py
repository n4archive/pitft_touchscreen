# !/usr/bin/python
#  -*- coding: utf-8 -*-

from pitft_touchscreen import pitft_touchscreen
from time import sleep

# Init touchscreen
t = pitft_touchscreen()
# Init collecting events
t.start()

while True:
    # Handle waiting events
    while not t.queue_empty():
        for e in t.get_event():
            print("Event received: {}".format(e))
    # Do your own business now
    print("Do whaterer you want to do while waiting for touchscreen events")
    # Wait ia second..
    sleep(1)

# In real program you need to call stop to stop collecting events
t.stop()
