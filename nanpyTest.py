from nanpy import Servo
import time
servo = Servo(9)
for move in [0,97,98,99,100,0]:
    print move
    servo.write(move)
    time.sleep(0.5)
