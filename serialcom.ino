#include <Servo.h>

char buffer[16];
int  bufferIndex = 0;
int servoxpos=0;
int servoypos=0;
Servo myServox;
Servo myServoy;
String readString="";
String initializer="";
String servox="";
String servoy="";
void setup()
{
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  myServox.attach(9);
  myServoy.attach(10); 
  Serial.begin(9600);
  Serial.println("Testing Serial");
}

void loop() {

  while (Serial.available()) {
    delay(10);
    if (Serial.available() >0) {
  char c = Serial.read();  //gets one byte from serial buffer
  readString += c; //makes the string readString
    }
  }

  if (readString.length() >0) {
  initializer = readString.substring(0, 1);
  servox = readString.substring(1, 4);
  servoy = readString.substring(5,8);
         

  int n1=0; //declare as number
  int n2=0;
        if (initializer == "(")
        {
          if (servox == "pos")
          {
            Serial.println();
            Serial.print("current pan position is ");
            Serial.print(servoxpos);
            Serial.println();
            Serial.print("current tilt position is ");
            Serial.print(servoypos);
            readString="";
          }
          else
          {  
            char carray1[4];
            servox.toCharArray(carray1, sizeof(carray1));
            n1 = atoi(carray1);
            servoxpos=n1;
            n1=map(n1,0,180,1000,2000);
            myServox.writeMicroseconds(n1);
                        
            char carray2[4];
            servoy.toCharArray(carray2, sizeof(carray2));
            n2 = atoi(carray2);
            servoypos=n2;
            n2=map(n2,0,180,1000,2000);
            myServoy.writeMicroseconds(n2);
            readString="";
          }
        }
}
}
