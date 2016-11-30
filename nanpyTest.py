from nanpy import Servo
import time
servo1 = Servo(5)
servo2 = Servo(9)

##servo1.write(0)
##print servo1.read()
##servo2.write(0)

##servo2.writeMicroseconds(1430)
##servo1.writeMicroseconds(1430)
##print servo1.read()
##time.sleep(1)
####
##servo2.write(20)
##servo1.write(20)

##servo1.write(0)
##servo2.write(0)


        
for move in range(544,2400):
    print move
    servo2.writeMicroseconds(move)
    servo1.writeMicroseconds(move)
    print servo1.read()
    print servo2.read()
    time.sleep(0.01)

    
servo1.write(0)
servo2.write(0)
##
##del servo1
##del servo2
    
