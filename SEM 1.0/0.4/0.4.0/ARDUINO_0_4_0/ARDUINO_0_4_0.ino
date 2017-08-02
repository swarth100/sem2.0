int LedPin = 2;
int Pin0 = 2; 
int Pin1 = 3; 
int Pin2 = 4; 
int Pin3 = 5; 
int sensorValue1;  // Right motor END
int sensorLow1 = 1023;
int sensorHigh1 = 0;
int turns = 0;
char command = ' ';
char input = ' ';

void setup () {
  pinMode(LedPin, OUTPUT);
  pinMode(Pin0, OUTPUT);  
  pinMode(Pin1, OUTPUT);  
  pinMode(Pin2, OUTPUT);  
  pinMode(Pin3, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin (9600);
}

void loop (){
  sensorValue1 = analogRead(A0);
  if (sensorValue1 > sensorHigh1) {
    sensorHigh1 = sensorValue1;
  }
  if (sensorValue1 < sensorLow1) {
    sensorLow1 = sensorValue1;
  }
  while (Serial.available()>1){
    input = Serial.read();
    command = Serial.read();
  }
  if (input == '0'){
    digitalWrite(LedPin, HIGH);
    if (command == '0'){
      turns = 100;
    }
     else if (command == '1'){
       turns = 1000;
     }
     for(int i=0; i<turns; i++){
       sensorValue1 = analogRead(A0);
       if (sensorValue1>= 200){
         Serial.print('1');
         Serial.print('5');
         break;
       }
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, LOW);
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, HIGH);
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, HIGH); 
       digitalWrite(Pin3, HIGH); 
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, HIGH); 
       digitalWrite(Pin3, LOW); 
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, HIGH); 
       digitalWrite(Pin2, HIGH); 
       digitalWrite(Pin3, LOW);
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, HIGH); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, LOW);
       delay(1);
       digitalWrite(Pin0, HIGH);  
       digitalWrite(Pin1, HIGH); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, LOW);
       delay(1);
       digitalWrite(Pin0, HIGH);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, LOW);
       delay(1);
       digitalWrite(Pin0, HIGH);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, HIGH);
       delay(1);
       digitalWrite(Pin0, LOW);  
       digitalWrite(Pin1, LOW); 
       digitalWrite(Pin2, LOW); 
       digitalWrite(Pin3, LOW);
       delay(1);
     }
   input = ' ';
   //delay(500);
  }
  else{
    digitalWrite(LedPin, LOW);
    input = ' ';
  }
}
