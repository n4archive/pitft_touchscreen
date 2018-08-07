#!/usr/bin/python
# -*- coding: utf-8 -*-

from pitft_touchscreen import pitft_touchscreen

t = pitft_touchscreen()
t.start()
for event_no in range(0, 10):
    event = t.events.get()
    print(event)
t.stop()
