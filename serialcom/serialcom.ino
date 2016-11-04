#include <Servo.h>

char c;
int servoxpos=0;
int servoypos=0;
int dist = 0;
Servo myServox;
Servo myServoy;
String readString="";
String initializer="";
String servox="";
String servoy="";
String dists ="";

void setup()
{
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  myServox.attach(9);
  myServoy.attach(10); 
  Serial.begin(9600);
  Serial.println("Testing Serial");
  
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.println('A');   // send a capital A to establish contact
    delay(300);
  }
}

void readserial(){
    while (Serial.available()>0 && c!=")") {
    c = Serial.read();  //gets one byte from serial buffer
    readString += c; //makes the string readString  
    }
    c = ""; //empty character buffer
}

void parsepacket(){
    readString.trim();
    initializer = readString.substring(0,1);
    if(initializer=="("){
      Serial.print(readString);
      servox = readString.substring(1,4);
      servoy = readString.substring(5,8);
      dists=readString.substring(9,12);       
  
  //      Serial.print(servox);
      
      char carray1[4];
      char carray2[4];
      char carray3[4];
      
      servox.toCharArray(carray1, sizeof(carray1));
      servoy.toCharArray(carray2, sizeof(carray2));
      dists.toCharArray(carray3, sizeof(carray3));
  
      Serial.print(carray1);
      
      servoxpos = atoi(carray1);
      servoypos = atoi(carray2);
      dist = atoi(carray3);
      Serial.print(servoxpos);      
    }

    readString="";

}

void moveservo(){
  int n1 = map(servoxpos,0,180,1000,2000);
  int n2 = map(servoypos,0,180,1000,2000);
  myServox.writeMicroseconds(n1);
  myServoy.writeMicroseconds(n2);
}


void loop() {
//  establishContact();
  readserial();
  parsepacket();
  Serial.print("(");
  Serial.print(servoxpos);
  Serial.print(",");
  Serial.print(servoypos);
  Serial.print(",");
  Serial.print(dist);
  Serial.println(")");  
  Serial.flush();
  delay(200);
  moveservo();
}
