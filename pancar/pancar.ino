#include <Servo.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

//Creating motor shield object w/ default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();

//setting the motor
Adafruit_DCMotor *motorR = AFMS.getMotor(4); //right motor
Adafruit_DCMotor *motorL = AFMS.getMotor(1); //left motor

Servo servo1;

char incomingByte = 0;
String packet = "";
int append = 0;

float dist = 0.0;

float ang1 = 0.0;
float ang2 = 0.0;

float updateRate = 0.5;





boolean dstFlag = True;
float initDist = 0;
boolean firstDistFlag = True;
float distThreshold = 0.5;
float distToTarget = 10;
float speedCons = 0.5;


boolean angFlag = False;
float initAng = 0;
boolean firstAngFlag = False;
float angThreshold = 0.5;
float angCons = 0.5;






void setup() {
  servo1.attach(9);
  Serial.begin(9600); //setting up Serial library at 9600 bps
  servo1.write(30);
  establishContact();
  AFMS.begin(); //create with default frequency 1.6kHz
  //starting direction (forward, backward, release)
  motorL->run(FORWARD);
  motorR->run(BACKWARD);
}

void goStraight() {
  motorR->setSpeed(20);
  motorL->setSpeed(20);
}

void turnLeft() {
  motorR->setSpeed(40);
  motorL->setSpeed(20);
}

void turnRight() {
  motorR->setSpeed(20);
  motorL->setSpeed(40);
}

void establishContact() {
  while (Serial.available() <= 0) {
    Serial.print('A');   // send a capital A
    delay(300);
  }
}

void parsepacket(String packet1) {
  int len = packet1.length();
  packet1.remove(0, 1);
  packet1[len - 2] = '\0';
  int cmaIdx = packet1.indexOf(',');
  int scmaIdx = packet1.indexOf(',', cmaIdx + 1);
  String sTheta = packet1.substring(0, cmaIdx - 1);
  String sPhi = packet1.substring(cmaIdx + 2, scmaIdx);
  String sDist = packet1.substring(scmaIdx + 2);
  sTheta.trim();
  sPhi.trim();
  sDist.trim();
  Serial.print("before:");
  Serial.print(sTheta);
  Serial.print(" ");
  Serial.print(sPhi);
  Serial.print(" ");
  Serial.println(sDist);
  //    String sThetat= "80.9";
  //    String sPhit = "91.05";
  //    String sDistt = "60.1";

  ang1 = sTheta.toInt();
  ang2 = sPhi.toInt();
  dist = sDist.toInt();
//  Serial.print("after:");
//  Serial.print(ang1);
//  Serial.print("\t");
//  Serial.print(ang2);
//  Serial.print("\t");
//  Serial.println(dist);
}

void loop() {
  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte == ';') {
      parsepacket(packet);


//// distance checking and setting speed
//     if(firstDistFlag == True){
//        initDist = dist;
//        firstDistFlag = False;
//      }
//      if(dstFlag == True){
//        speed1 = speedCons * (dist - distToTarget);
//        speed2 = speedCons * (dist - distToTarget);
//        if(dist - initDist*updateRate < distThreshold){
//          dstFlag = False;
//          angFlag = True;
//          firstAngFlag = True;
//         }        
//        }
////////////////////////////////////////
//
//// angle checking and setting speed       
//     if(firstAngFlag == True){
//        initAng = ang1;
//        firstAngFlag = False;
//      }
//      if(angFlag == True){
//        if(ang1 > 0){
//          speed1 = angCons * ang1;
//          speed2 = 0;
//          }else{
//          speed2 = angCons * abs(ang1)
//          speed1 = 0;
//            }
//        if(ang1 - initAng*updateRate < angThreshold){
//          angFlag = False;
//          distFalg = True;
//          firstDistFlag = True;
//         }        
//        }

//////////////////////////////////////        



      

      if (dist <= 10) {             // if there is not detected face(dist = 0) or the distance is too close, break
        break;
      }
      else {
        if (ang1 >= -5 and ang1 <= 5) {
          goStraight();
        }
        else if (ang1 >= 0) {
          turnRight();
          vr = 20;
          vl = 20 + cons * (ang1 - 5);
        }
        else if (ang1 <= 0) {
          turnLeft();
          vl = 20;
          vr = 20 + cons * (abs(ang1) - 5);
        }
      }

      packet = "";

    }
    else {
      packet += incomingByte;
    }
  }
  else {
    establishContact();
  }
}
