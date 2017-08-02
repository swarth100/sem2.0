int LedPin = 2;
int Pin0 = 2; 
int Pin1 = 3; 
int Pin2 = 4; 
int Pin3 = 5; 
int Resistor1;
int Resistor2;
int Resistor3;
int Resistor4;
int turns = 0;
int right_step = 0;
int left_step = 0;
char command = ' ';
char input = ' ';
char verse = ' ';
boolean Photo_pressed1 = false;
boolean Photo_pressed2 = false;
boolean Photo_pressed3 = false;
boolean Photo_pressed4 = false;

void setup () {
  pinMode(LedPin, OUTPUT);
  pinMode(Pin0, OUTPUT);  
  pinMode(Pin1, OUTPUT);  
  pinMode(Pin2, OUTPUT);  
  pinMode(Pin3, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  Serial.begin (9600);
}

void loop (){
  if (Serial.available()>=3){
    input = Serial.read();
    command = Serial.read();
    verse = Serial.read();
  }
  if (input == '1'){
    Serial.print(input);
    Serial.print(command);
    Serial.print(verse);
  }
  if (input == '0'){
    //digitalWrite(LedPin, HIGH);
    if (command == '0'){
      Pin0 = 2; 
      Pin1 = 3; 
      Pin2 = 4; 
      Pin3 = 5; 
      turns = 10000;
    }
    if (command == '1'){
      Pin0 = 2; 
      Pin1 = 3; 
      Pin2 = 4; 
      Pin3 = 5; 
      turns = right_step;
    }
    if (command == '2'){
      Pin0 = 6; 
      Pin1 = 7; 
      Pin2 = 8; 
      Pin3 = 9; 
      turns = 10000;
    }
    if (command == '3'){
      Pin0 = 6; 
      Pin1 = 7; 
      Pin2 = 8; 
      Pin3 = 9; 
      turns = left_step;
    }
    if (command == '4'){
      Pin0 = 2; 
      Pin1 = 3; 
      Pin2 = 4; 
      Pin3 = 5; 
      turns = right_step/2;
    }
    if (command == '5'){
      Pin0 = 6; 
      Pin1 = 7; 
      Pin2 = 8; 
      Pin3 = 9; 
      turns = left_step/2;
    }
    Photo_pressed1 = true;
    Photo_pressed2 = true;
    Photo_pressed3 = true;
    Photo_pressed4 = true;
    for(int i=0; i<turns; i++){
      Resistor1 = analogRead(A0);
      Resistor2 = analogRead(A1);
      Resistor3 = analogRead(A2);
      Resistor4 = analogRead(A3);
      if (Resistor1 >= 900){
        if (Photo_pressed1 == false){
          Serial.print('1');
          Serial.print('0');
          Serial.print(verse);
          Photo_pressed1 = true;
          if (command == '0'){
            right_step = (int) (i/10);
          }
          break;
        }
      }
      else{
        if (Resistor1 < 900){
          Photo_pressed1 = false;
        }
      }
      if (Resistor2 >= 900){
        if (Photo_pressed2 == false){
          Serial.print('1');
          Serial.print('1');
          Serial.print(verse);
          Photo_pressed2 = true;
          if (command == '0'){
            right_step = (right_step*10 + i)/20;
          }
          break;
        }
      }
      else{
        if (Resistor2 < 900){
          Photo_pressed2 = false;
        }
      }
      if (Resistor3 >= 900){
        if (Photo_pressed3 == false){
          Serial.print('1');
          Serial.print('3');
          Serial.print(verse);
          Photo_pressed3 = true;
          if (command == '2'){
            left_step = (int) (i/10);
          }
          break;
        }
      }
      else{
        if (Resistor3 < 900){
          Photo_pressed3 = false;
        }
      }
      if (Resistor4 >= 900){
        if (Photo_pressed4 == false){
          Serial.print('1');
          Serial.print('4');
          Serial.print(verse);
          Photo_pressed4 = true;
          if (command == '2'){
            left_step = (left_step*10 + i)/20;
          }
          break;
        }
      }
      else{
        if (Resistor4 < 900){
          Photo_pressed4 = false;
        }
      }
      if (verse == '0'){
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
      else if (verse == '1'){
        digitalWrite(Pin0, LOW);  
        digitalWrite(Pin1, LOW); 
        digitalWrite(Pin2, LOW); 
        digitalWrite(Pin3, LOW);
        delay(1);
        digitalWrite(Pin0, HIGH);  
        digitalWrite(Pin1, LOW); 
        digitalWrite(Pin2, LOW); 
        digitalWrite(Pin3, HIGH);
        delay(1);
        digitalWrite(Pin0, HIGH);  
        digitalWrite(Pin1, LOW); 
        digitalWrite(Pin2, LOW); 
        digitalWrite(Pin3, LOW);
        delay(1);
        digitalWrite(Pin0, HIGH);  
        digitalWrite(Pin1, HIGH); 
        digitalWrite(Pin2, LOW); 
        digitalWrite(Pin3, LOW);
        delay(1);
        digitalWrite(Pin0, LOW);  
        digitalWrite(Pin1, HIGH); 
        digitalWrite(Pin2, LOW); 
        digitalWrite(Pin3, LOW);
        delay(1);
        digitalWrite(Pin0, LOW);  
        digitalWrite(Pin1, HIGH); 
        digitalWrite(Pin2, HIGH); 
        digitalWrite(Pin3, LOW);
        delay(1);
        digitalWrite(Pin0, LOW);  
        digitalWrite(Pin1, LOW); 
        digitalWrite(Pin2, HIGH); 
        digitalWrite(Pin3, LOW); 
        delay(1);
        digitalWrite(Pin0, LOW);  
        digitalWrite(Pin1, LOW); 
        digitalWrite(Pin2, HIGH); 
        digitalWrite(Pin3, HIGH); 
        delay(1);
        digitalWrite(Pin0, LOW);  
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
      if ((i + 1) == turns){
        Serial.print('1');
        Serial.print('2');
        Serial.print(verse);
      }
    }
  input = ' ';
  command = ' ';
  verse = ' ';
  }
  else{
    //digitalWrite(LedPin, LOW);
    input = ' ';
    command = ' ';
    verse = ' ';
  }
}
