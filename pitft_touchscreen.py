#!/usr/bin/python
# -*- coding: utf-8 -*-
#  piTFT touchscreen handling using evdev

import evdev

## Class for handling events from piTFT
class pitft_touchscreen():
    def __init__(self, device_path="/dev/input/touchscreen"):
        self.device = evdev.InputDevice(device_path)
        if self.device is not None:
            print("Input device {} found".format(device_path))
        else:
            print("Input device {} not found".format(device_path))
            exit()
        self.event = {}
        self.event['time'] = None
        self.event['x'] = None
        self.event['y'] = None
        self.event['id'] = None
        self.event['touch'] = None

    def event_loop(self):
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.event['x'] = event.value
                elif event.code == evdev.ecodes.ABS_Y:
                    self.event['y'] = event.value
                elif event.code == evdev.ecodes.ABS_MT_TRACKING_ID:
                    self.event['id'] = event.value
                elif event.code == evdev.ecodes.ABS_MT_POSITION_X:
                    pass
                elif event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                    pass
            elif event.type == evdev.ecodes.EV_KEY:
                self.event['touch'] = event.value
            elif event.type == evdev.ecodes.SYN_REPORT:
                self.event['time'] = event.timestamp()
                print(self.event)
