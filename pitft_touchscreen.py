#!/usr/bin/python
# -*- coding: utf-8 -*-
#  piTFT touchscreen handling using evdev

import evdev
import queue
import threading


# Class for handling events from piTFT
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
                elif event.code == evdev.ecodes.ABS_MT_POSITION_X:
                    pass
                elif event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                    pass
            elif event.type == evdev.ecodes.EV_KEY:
                self.event['touch'] = event.value
            elif event.type == evdev.ecodes.SYN_REPORT:
                self.event['time'] = event.timestamp()
                self.events.put(self.event)
                # Keep old values
                old_event = self.event
                self.event = {}
                self.event['x'] = old_event['x']
                self.event['y'] = old_event['x']
                self.event['id'] = old_event['id']
                self.event['touch'] = old_event['touch']

    def get_event(self):
        if not self.events.empty():
            event = self.events.get()
            yield event
        else:
            yield None

    def queue_empty(self):
        return self.events.empty()

    def stop(self):
        self.stopping = True
        # Inject event to force immediate breaking "for" loop in run procedure.
        self.device.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X, 1)
        self.device.write(evdev.ecodes.SYN_REPORT, 0, 0)

    def __del__(self):
        self.stop()
