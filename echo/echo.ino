int append = 0;
char incomingByte = 0;
String packet = "";
void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

 
void loop() {  
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        if(incomingByte ==';'){
          Serial.println(packet);
          packet="";
        }
        else{
          packet+=incomingByte;
        }
    }               
}
