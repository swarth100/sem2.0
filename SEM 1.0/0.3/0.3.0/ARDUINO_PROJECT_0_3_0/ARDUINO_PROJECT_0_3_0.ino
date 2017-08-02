int units = 0;
int motorPin1 = 2;
int motorPin2 = 3;
int motorPin3 = 4;
int motorPin4 = 5;
int sensorValue1;  // Right motor END
int sensorLow1 = 1023;
int sensorHigh1 = 0;
int sensorValue2;  // Right motor START
int sensorLow2 = 1023;
int sensorHigh2 = 0;
int sensorValue3;  // Left motor END
int sensorLow3 = 1023;
int sensorHigh3 = 0;
int sensorValue4;  // Left motor START
int sensorLow4 = 1023;
int sensorHigh4 = 0;

void setup (){
  Serial.begin (9600);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
}

void loop (){
  sensorValue1 = analogRead(A0);
    if (sensorValue1 > sensorHigh1) {
      sensorHigh1 = sensorValue1;
    }
    if (sensorValue1 < sensorLow1) {
      sensorLow1 = sensorValue1;
    }
    sensorValue2 = analogRead(A1);
    if (sensorValue2 > sensorHigh2) {
      sensorHigh2 = sensorValue2;
    }
    if (sensorValue2 < sensorLow2) {
      sensorLow2 = sensorValue2;
    }
    sensorValue3 = analogRead(A2);
    if (sensorValue3 > sensorHigh3) {
      sensorHigh3 = sensorValue3;
    }
    if (sensorValue3 < sensorLow3) {
      sensorLow3 = sensorValue3;
    }
    sensorValue4 = analogRead(A3);
    if (sensorValue4 > sensorHigh4) {
      sensorHigh4 = sensorValue4;
    }
    if (sensorValue4 < sensorLow4) {
      sensorLow4 = sensorValue4;
    }
  if ( Serial.available() == 4){
    char author = Serial.read();
    char command_1 = Serial.read();
    char command_2 = Serial.read();
    char command_3 = Serial.read();
    if (command_3 != ' '){
      units = (command_3 - '0');
    }
    if (author == 'python\n'){
      int movement = units;
      int verse = 0;
      if (command_1 == '/moveright\n'){
        motorPin1 = 2;
        motorPin2 = 3;
        motorPin3 = 4;
        motorPin4 = 5;
        if (command_1 == '/clockwise\n'){
          movement = units;
        }
        else{
          verse = 1;
        }
        for (int times_turned = 1; times_turned < units; times_turned ++){
          if (verse == 0){
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, HIGH);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, HIGH);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, HIGH);
          }
          else{
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, HIGH);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, HIGH);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, HIGH);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
          }
        }
        if (sensorHigh1 > (sensorLow1 + 100)){
          Serial.print('/arduino\n');
          Serial.print('/end_right\n');
          Serial.print('\n');
          Serial.print(' ');
          sensorLow1 = 1023;
          sensorHigh1 = 0;
        }
        else{
          if (sensorHigh2 > (sensorLow2 + 100)){
            Serial.print('/arduino\n');
            Serial.print('/start_right\n');
            Serial.print('\n');
            Serial.print(' ');
            sensorLow2 = 1023;
            sensorHigh2 = 0;
          }
          else{
            Serial.print('/arduino\n');
            Serial.print('/stopped_right\n');
            Serial.print('\n');
            Serial.print(' ');
            sensorLow1 = 1023;
            sensorHigh1 = 0;
            sensorLow2 = 1023;
            sensorHigh2 = 0;
          }
        }
      }
      if (command_1 == '/moveleft\n'){
        motorPin1 = 6;
        motorPin2 = 7;
        motorPin3 = 8;
        motorPin4 = 9;
        if (command_1 == '/clockwise\n'){
          movement = units;
        }
        else{
          verse = 1;
        }
        for (int times_turned = 1; times_turned < units; times_turned ++){
          if (verse == 0){
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, HIGH);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, HIGH);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, HIGH);
          }
          else{
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, HIGH);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, HIGH);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, LOW);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, HIGH);
            digitalWrite(motorPin4, LOW);
            
            digitalWrite(motorPin1, HIGH);
            digitalWrite(motorPin2, LOW);
            digitalWrite(motorPin3, LOW);
            digitalWrite(motorPin4, LOW);
          }
        }
        if (sensorHigh3 > (sensorLow3 + 100)){
          Serial.print('/arduino\n');
          Serial.print('/end_left\n');
          Serial.print('\n');
          Serial.print(' ');
          sensorLow3 = 1023;
          sensorHigh3 = 0;
        }
        else{
          if (sensorHigh4 > (sensorLow4 + 100)){
            Serial.print('/arduino\n');
            Serial.print('/start_left\n');
            Serial.print('\n');
            Serial.print(' ');
            sensorLow4 = 1023;
            sensorHigh4 = 0;
          }
          else{
            Serial.print('/arduino\n');
            Serial.print('/stopped_right\n');
            Serial.print('\n');
            Serial.print(' ');
            sensorLow3 = 1023;
            sensorHigh3 = 0;
            sensorLow4 = 1023;
            sensorHigh4 = 0;
          }
        }
      }
    }
  }
}
