import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
<<<<<<< HEAD
    port='/dev/ttyACM0',
=======
    port='/dev/cu.usbmodem1411',
>>>>>>> 17d56b2d116ec7e9182445716ef0a466ede2d9f3
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

if ser.isOpen():
    print 'Enter your commands below.\r\nInsert "exit" to leave the application.'
    # while ser.inWaiting()>0:
        

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
<<<<<<< HEAD
        ser.write(str(input))
=======
        ser.write(input)
        print input
>>>>>>> 17d56b2d116ec7e9182445716ef0a466ede2d9f3
        out = ''
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(1)
        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">>" + out