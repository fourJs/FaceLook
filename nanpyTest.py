# /nanpy/examples/servo.py
#!/usr/bin/env python
# Author: Andrea Stagi <stagi.andrea@gmail.com>
# Description: move a servo motor
# Dependencies: None
from nanpy import Servo
import time

servo1 = Servo(6)
servo2 = Servo(9)

servo1.write(20)
time.sleep(1)
print "wrote to servo1"
servo2.write(20)
print "wrote to servo2"
time.sleep(3)


    
servo1.write(0)
servo2.write(0)
print "done"
##
##del servo1
##del servo2
    
