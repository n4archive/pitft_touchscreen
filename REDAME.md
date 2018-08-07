Very simple piTFT touchscreen handling class. Usage:
```
pi@raspberrypi:~/pitft_touchscreen $ python3
Python 3.4.2 (default, Oct 19 2014, 13:31:11) 
[GCC 4.9.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pitft_touchscreen import pitft_touchscreen
>>> t = pitft_touchscreen()
Input device /dev/input/touchscreen found
>>> t.event_loop()
{'x': 107, 'y': 196, 'id': 28, 'touch': 1, 'time': 1533598922.222931}
{'x': 105, 'y': 194, 'id': 28, 'touch': 1, 'time': 1533598922.290021}
{'x': 103, 'y': 192, 'id': 28, 'touch': 1, 'time': 1533598922.326449}
{'x': 101, 'y': 192, 'id': 28, 'touch': 1, 'time': 1533598922.338607}
{'x': 99, 'y': 191, 'id': 28, 'touch': 1, 'time': 1533598922.362882}
{'x': 97, 'y': 191, 'id': 28, 'touch': 1, 'time': 1533598922.399298}
{'x': 96, 'y': 193, 'id': 28, 'touch': 1, 'time': 1533598922.435757}
{'x': 95, 'y': 196, 'id': 28, 'touch': 1, 'time': 1533598922.460071}
{'x': 95, 'y': 198, 'id': 28, 'touch': 1, 'time': 1533598922.484332}
{'x': 95, 'y': 200, 'id': 28, 'touch': 1, 'time': 1533598922.532955}
{'x': 97, 'y': 199, 'id': 28, 'touch': 1, 'time': 1533598922.617916}
{'x': 99, 'y': 198, 'id': 28, 'touch': 1, 'time': 1533598922.71514}
{'x': 100, 'y': 200, 'id': 28, 'touch': 1, 'time': 1533598922.739466}
{'x': 102, 'y': 202, 'id': 28, 'touch': 1, 'time': 1533598922.775854}
{'x': 103, 'y': 204, 'id': 28, 'touch': 1, 'time': 1533598922.812303}
{'x': 104, 'y': 206, 'id': 28, 'touch': 1, 'time': 1533598922.860857}
{'x': 105, 'y': 208, 'id': 28, 'touch': 1, 'time': 1533598922.958037}
{'x': 105, 'y': 208, 'id': -1, 'touch': 0, 'time': 1533598923.042836}
```
Another example with touchscreen file in initialisation call:
```
>>> from pitft_touchscreen import pitft_touchscreen
>>> t = pitft_touchscreen("/dev/input/event0")
Input device /dev/input/event0 found
>>> t.event_loop()
{'id': 29, 'touch': 1, 'x': 120, 'time': 1533599037.254026, 'y': 173}
{'id': -1, 'touch': 0, 'x': 120, 'time': 1533599037.296873, 'y': 173}
{'id': 30, 'touch': 1, 'x': 49, 'time': 1533599038.656337, 'y': 148}
{'id': 30, 'touch': 1, 'x': 49, 'time': 1533599038.742343, 'y': 150}
{'id': 30, 'touch': 1, 'x': 49, 'time': 1533599038.766624, 'y': 152}
{'id': 30, 'touch': 1, 'x': 49, 'time': 1533599038.778809, 'y': 154}
{'id': 30, 'touch': 1, 'x': 49, 'time': 1533599038.803076, 'y': 157}
{'id': 30, 'touch': 1, 'x': 48, 'time': 1533599038.827294, 'y': 160}
{'id': -1, 'touch': 0, 'x': 48, 'time': 1533599038.839382, 'y': 160}
```
