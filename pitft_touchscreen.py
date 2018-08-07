#!/usr/bin/python
# -*- coding: utf-8 -*-
#  piTFT touchscreen handling using evdev

import evdev
import queue
import threading


## Class for handling events from piTFT
class pitft_touchscreen(threading.Thread):
    def __init__(self, device_path="/dev/input/touchscreen"):
        super(pitft_touchscreen, self).__init__()
        self.device = evdev.InputDevice(device_path)
        if self.device is not None:
            print("Input device {} found".format(device_path))
        else:
            print("Input device {} not found".format(device_path))
            exit()
        self.event = {}
        self.reset_state()
        self.events = queue.Queue()

    def run(self):
        self.stopping = False
        for event in self.device.read_loop():
            if self.stopping:
                break
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.event['x'] = event.value
                elif event.code == evdev.ecodes.ABS_Y:
                    self.event['y'] = event.value
                elif event.code == evdev.ecodes.ABS_MT_TRACKING_ID:
                    self.event['id'] = event.value
                    if event.value == -1:
                        self.reset_state_required = True
                elif event.code == evdev.ecodes.ABS_MT_POSITION_X:
                    pass
                elif event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                    pass
            elif event.type == evdev.ecodes.EV_KEY:
                self.event['touch'] = event.value
            elif event.type == evdev.ecodes.SYN_REPORT:
                self.event['time'] = event.timestamp()
                self.events.put(self.event)
                if self.reset_state_required:
                    self.reset_state()

    def reset_state(self):
        self.event = {}
        self.event['time'] = None
        self.event['x'] = None
        self.event['y'] = None
        self.event['id'] = None
        self.event['touch'] = None
        self.reset_state_required = False

    def stop(self):
        self.stopping = True
        #Inject event to force immediate breaking for loop in run procedure.
        self.device.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X, 1)
        self.device.write(evdev.ecodes.SYN_REPORT, 0, 0)

    def __del__(self):
        self.stop()
