#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  piTFT touchscreen handling using evdev for resistive and capacitive screens.

try:
    import evdev
except ImportError:
    print("evdev package is not installed.  Run 'pip3 install evdev' (python3) or 'pip install evdev' to install.")
    raise(ImportError("evdev package not found"))
import threading
try:
    # python 3.5+
    import queue
except ImportError:
    # python 2.7
    import Queue as queue


# Class for handling events from piTFT
class pitft_touchscreen(threading.Thread):
    def __init__(self, device_path="/dev/input/touchscreen", grab=False):
        super(pitft_touchscreen, self).__init__()
        self.device_path = device_path
        self.grab = grab
        self.events = queue.Queue()
        self.shutdown = threading.Event()
        self.devices_resistive = ["EP0110M09"]    # Support for Adafruit 2.8 Capacitive PiTFT
        self.devices_capacitive = ["stmpe-ts"]    # Support for Adafruit 2.4, 2.8, 3.2, 3.5 Resistive PiTFT

    def run(self):
        thread_process = threading.Thread(target=self.process_device)
        # run thread as a daemon so it gets cleaned up on exit.
        thread_process.daemon = True
        thread_process.start()
        self.shutdown.wait()

    # thread function
    def process_device(self):
        device = None
        # if the path to device is not found, InputDevice raises an OSError
        # exception.  This will handle it and close thread.
        try:
            device = evdev.InputDevice(self.device_path)
            if self.grab:
                device.grab()
        except Exception as ex:
            message = "Unable to load device {0} due to a {1} exception with" \
                      " message: {2}.".format(self.device_path,
                                              type(ex).__name__, str(ex))
            raise Exception(message)
        finally:
            if device is None:
                self.shutdown.set()
        if device.name in self.devices_capacitive:
            self.capacitive_device(device)
        elif device.name in self.devices_resistive:
            self.resistive_device(device)
        else:
            if self.grab:
                device.ungrab()
            raise OSError("Unsupported evdev device: {}".format(device.name))
        if self.grab:
            device.ungrab()

    def capacitive_device(self, device):
        event = {'time': None, 'id': None, 'x': None, 'y': None, 'touch': None}
        dropping = False
        while not self.shutdown.is_set():
            for input_event in device.read_loop():
                if input_event.type == evdev.ecodes.EV_ABS:
                    if input_event.code == evdev.ecodes.ABS_X:
                        event['x'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_Y:
                        event['y'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_MT_TRACKING_ID:
                        event['id'] = input_event.value
                        if input_event.value == -1:
                            event['x'] = None
                            event['y'] = None
                            event['touch'] = None
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_X:
                        pass
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                        pass
                elif input_event.type == evdev.ecodes.EV_KEY:
                    event['touch'] = input_event.value
                elif input_event.type == evdev.ecodes.SYN_REPORT:
                    if dropping:
                        event['x'] = None
                        event['y'] = None
                        event['touch'] = None
                        dropping = False
                    else:
                        event['time'] = input_event.timestamp()
                        self.events.put(event)
                        e = event
                        event = {'x': e['x'], 'y': e['y']}
                        try:
                            event['id'] = e['id']
                        except KeyError:
                            event['id'] = None
                        try:
                            event['touch'] = e['touch']
                        except KeyError:
                            event['touch'] = None
                elif input_event.type == evdev.ecodes.SYN_DROPPED:
                    dropping = True

    def resistive_device(self, device):
        event = {'time': None, 'id': None, 'x': None, 'y': None, 'touch': None, 'pressure': None}
        dropping = False
        while not self.shutdown.is_set():
            for input_event in device.read_loop():
                if input_event.type == evdev.ecodes.EV_ABS:
                    if input_event.code == evdev.ecodes.ABS_X:
                        event['x'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_Y:
                        event['y'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_PRESSURE:
                        event['pressure'] = input_event.value
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_X:
                        pass
                    elif input_event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                        pass
                elif input_event.type == evdev.ecodes.EV_KEY:
                    event['touch'] = input_event.value
                elif input_event.type == evdev.ecodes.SYN_REPORT:
                    if dropping:
                        event['x'] = None
                        event['y'] = None
                        dropping = False
                    else:
                        if input_event.sec is not None and input_event.usec is not None:
                            event['id'] = "{0}.{1}".format(input_event.sec, input_event.usec)
                        event['time'] = input_event.timestamp()
                        self.events.put(event)
                        e = event
                        event = {'x': e['x'], 'y': e['y']}
                        try:
                            event['pressure'] = e['pressure']
                        except KeyError:
                            event['pressure'] = None
                        try:
                            event['id'] = e['id']
                        except KeyError:
                            event['id'] = None
                        try:
                            event['touch'] = e['touch']
                        except KeyError:
                            event['touch'] = None
                    event['x'] = None
                    event['y'] = None
                    event['touch'] = None
                    event['pressure'] = None
                elif input_event.type == evdev.ecodes.SYN_DROPPED:
                    dropping = True

    def get_event(self):
        if not self.events.empty():
            event = self.events.get()
            yield event
        else:
            yield None

    def queue_empty(self):
        return self.events.empty()

    def stop(self):
        self.shutdown.set()

    def __del__(self):
        self.shutdown.set()
