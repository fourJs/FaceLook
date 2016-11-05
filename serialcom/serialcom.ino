#include <Servo.h>

int c;
int servoxpos=0;
int servoypos=0;
int dist = 0;
Servo myServox;
Servo myServoy;
int packet[12];

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
    Serial.print("A)");   // send a capital A
    delay(300);
  }
}
  
void readserial(){
    int i = 0;
    while (Serial.available()>0 && i<=12) {
      c = Serial.read();  //gets one byte from serial buffer
      packet[i] = c;
//      Serial.print(c);
      i++;
    }
    c = 0; //empty character buffer
}

int translate(int a){
  if(a>=176){
    return a-176;
  }
  else{
    return a-48;
  }
}

void parsepacket(){
  
    if(packet[0]==168){
      servoxpos = 100*(translate(packet[1]))+10*(translate(packet[2]))+(translate(packet[3]));
      servoypos = 100*(translate(packet[5]))+10*(translate(packet[6]))+(translate(packet[7]));
      dist = 100*(translate(packet[9]))+10*(translate(packet[10]))+(translate(packet[11]));  
    }    
}

void moveservo(){
  int n1 = map(servoxpos,0,180,1000,2000);
  int n2 = map(servoypos,0,180,1000,2000);
  myServox.writeMicroseconds(n1);
  myServoy.writeMicroseconds(n2);
}


void loop() {
  establishContact();
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
