int append = 0;
float packet[3] = {0.0,0.0,0.0};
void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}


void loop() {
  if (Serial.available() >0){
    if (Serial.read() == '('){
      append = 0;
    }
    else if (Serial.read() == ')'){
      append = -1;
    }
    if (append >=0){
      packet[append]=Serial.parseFloat();
      append+=1;  
    }
    if (append ==3){
      for (int i=0; i<3; i++){
        Serial.println(packet[i]);  
      }
    }
  }

  if(append==3){
    
  }
      
//    // send data only when you receive data:
//    if (Serial.available() > 0) {
//        // read the incoming byte:
//        incomingByte = Serial.read();
//        if (incomingByte =='(') {
//          append = 1;                  
//        }
//        else if(incomingByte == ')') {
//          packet += incomingByte;
//          append = 0;
//        }
//        if (append==1){
//              packet+= incomingByte;
//        }
//        else if(append==0 && incomingByte ==')') {
//            // say what you got:
//          Serial.print("I received: ");
//          Serial.println(packet);
//          packet = "";  
//        }          
//    }
               
}
