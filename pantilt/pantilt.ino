#include <Servo.h>

Servo servo1;
Servo servo2;

char incomingByte = 0;
String packet = "";
int append = 0;

//float ang1 = 0.0;
//float ang2 = 0.0;
float dist = 0.0;

float ang1_r = 0.0;
float ang2_r = 0.0;

//float ang1_0 = 0.0;
//float ang1_1 = 0.0;
//float ang2_0 = 0.0;
//float ang2_1 = 0.0;
//float delta_ang1;
//float delta_ang2;

void setup() {
  servo1.attach(9);
  servo2.attach(10);
  Serial.begin(9600);
  establishContact();
  
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}

void parsepacket(String packet1){
    int len = packet1.length();
    packet1.remove(0,1);
    packet1[len-1]='\0';
    packet1[len-2]='\0';
    int cmaIdx = packet1.indexOf(',');
    int scmaIdx = packet1.indexOf(',',cmaIdx+1);
    String sTheta = packet1.substring(0,cmaIdx-1);
    String sPhi = packet1.substring(cmaIdx+2,scmaIdx);
    String sDist = packet1.substring(scmaIdx+2);
    Serial.print("before:");
    Serial.print(sTheta);
    Serial.print(" ");
    Serial.print(sPhi);
    Serial.print(" ");
    Serial.println(sDist);
    ang1_r = sTheta.toFloat();
    ang2_r = sPhi.toFloat();
    dist = sDist.toFloat();
    Serial.print("after:");
    Serial.print(ang1_r);
    Serial.print("\t");
    Serial.print(ang2_r);
    Serial.print("\t");
    Serial.println(dist);
}

void loop() {
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        if(incomingByte ==';'){
          parsepacket(packet);
//          ang1_0 = ang1_1;
//          ang1_1 = ang1_r;
//          ang2_0 = ang2_1;
//          ang2_1 = ang2_r;
//        
//          delta_ang1 = ang1_1 - ang1_0;
//          delta_ang2 = ang2_1 - ang2_0;
//        
//          ang1 = ang1 + delta_ang1;
//          ang2 = ang2 + delta_ang2;
//          Serial.println(packet);      
//          Serial.println(ang1);
          Serial.println(ang1_r);
//          Serial.print("\t");
//          Serial.println(ang2_r);
          servo1.write(ang1_r);
          servo2.write(ang2_r); 
          packet="";
          
        }
        else{
          packet+=incomingByte;
        }
    }
    else{
      establishContact();
    }
}
   
  



////================================= motor =================================//
//
//#include <Wire.h>
//#include <Adafruit_MotorShield.h>
//#include "utility/Adafruit_MS_PWMServoDriver.h"
//
////Stack
////Creating motor shield object w/ default I2C address
//Adafruit_MotorShield AFMS = Adafruit_MotorShield();
//
////setting the motor
//Adafruit_DCMotor *motorR = AFMS.getMotor(2); //right motor
//Adafruit_DCMotor *motorL = AFMS.getMotor(1); //left motor
//
//int dist;
//
//void setup() {
//  //setup motor
//  Serial.begin(9600); //setting up Serial library at 9600 bps
//  AFMS.begin(); //create with default frequency 1.6kHz
//  //starting direction (forward, backward, release)
//  motorL->run(BACKWARD);
//  motorR->run(FORWARD);
//}
//
//void goStraight() {
//  motorR->setSpeed(20);
//  motorL->setSpeed(20);
//}
//
//void turnLeft() {
//  motorR->setSpeed(40);
//  motorL->setSpeed(20);
//}
//
//void turnRight() {
//  motorR->setSpeed(20);
//  motorL->setSpeed(40);
//}
//
//void loop() {
//  if (dist <= 10) {             // if there is not detected face(dist = 0? or -1?) or the distance is too close, break
//    break;
//  }
//  else {
//    if (ang1 >= -5 and ang1 <= 5) {
//      goStraight();
//    }
//    else if (ang1 >= 0) {
//      turnRight();
//    }
//    else if (ang1 <= 0) {
//      turnLeft();
//    }
//  }
//  Serial.print(dist);
//  Serial.print("\t");
//  Serial.print(ang1);
//  Serial.print("\t");
//  Serial.println(ang2);
//}
