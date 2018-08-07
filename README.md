Very simple piTFT touchscreen handling class. Fully threaded ;-)
Usage:
```
pi@raspberrypi:~/pitft_touchscreen $ python3
Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pitft_touchscreen import pitft_touchscreen
>>> t=pitft_touchscreen()
Input device /dev/input/touchscreen found
>>> t.start()
>>> for i in range(0,10):
...     t.events.get()
... 
{'y': 166, 'x': 96, 'time': 1533659492.336205, 'touch': 1, 'id': 172}
{'y': 164, 'x': 95, 'time': 1533659492.367231, 'touch': 1, 'id': 172}
{'y': 162, 'x': 94, 'time': 1533659492.379434, 'touch': 1, 'id': 172}
{'y': 159, 'x': 94, 'time': 1533659492.391555, 'touch': 1, 'id': 172}
{'y': 155, 'x': 93, 'time': 1533659492.403658, 'touch': 1, 'id': 172}
{'y': 152, 'x': 93, 'time': 1533659492.415846, 'touch': 1, 'id': 172}
{'y': 150, 'x': 93, 'time': 1533659492.427978, 'touch': 1, 'id': 172}
{'y': 148, 'x': 93, 'time': 1533659492.440117, 'touch': 1, 'id': 172}
{'y': 146, 'x': 93, 'time': 1533659492.452251, 'touch': 1, 'id': 172}
{'y': 144, 'x': 94, 'time': 1533659492.476523, 'touch': 1, 'id': 172}
>>> t.stop()
>>> exit()
pi@raspberrypi:~/pitft_touchscreen $
```
