import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
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
        a = str(input)

        ser.write(str.encode(a,"UTF-8"))
        out = ''

        while ser.inWaiting() > 0:
            out = ser.read(1)        

        if out != '':
            print ">>" + out