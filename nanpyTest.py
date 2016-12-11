# /nanpy/examples/servo.py
#!/usr/bin/env python
# Author: Andrea Stagi <stagi.andrea@gmail.com>
# Description: move a servo motor
# Dependencies: None
from nanpy import ArduinoApi
from nanpy import SerialManager
import time
from nanpy import Servo

connection = SerialManager(device='/dev/ttyACM0')

a = ArduinoApi(connection = connection)
a.pinMode(8, a.OUTPUT)
a.pinMode(9, a.OUTPUT)
a.pinMode(10, a.OUTPUT)
a.pinMode(11, a.OUTPUT)
a.pinMode(5, a.OUTPUT)
a.pinMode(6, a.OUTPUT)


a.digitalWrite(8, a.HIGH)
a.digitalWrite(9, a.LOW)

a.digitalWrite(10, a.HIGH)
a.digitalWrite(11, a.LOW)

# for move in range(100,255,4):
#     a.analogWrite(5, move)
#     time.sleep(0.5)
#     print move

a.analogWrite(5, 0)
a.analogWrite(6, 0)

servo_tilt = Servo(3)
servo_tilt.write(90)
##connection = np.SerialManager(device='/dev/ttyACM1')
##a = np.ArduinoApi(connection=connection)
##a.pinMode(13, a.OUTPUT)
##a.digitalWrite(13, a.HIGH)
