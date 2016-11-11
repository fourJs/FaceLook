from nanpy import Servo
import time
servo = Servo(11)
for move in [0, 90]:
    servo.write(move)
    time.sleep(1)
