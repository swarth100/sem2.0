int LedPin = 2;
int Pin0 = 2; 
int Pin1 = 3; 
int Pin2 = 4; 
int Pin3 = 5; 
int Resistor1;
int Resistor2;
int turns = 0;
int right_step = 0;
char command = ' ';
char input = ' ';
char verse = ' ';
boolean Photo_pressed1 = false;
boolean Photo_pressed2 = false;

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
      turns = 10000;
    }
    if (command == '1'){
      turns = right_step;
    }
    if (command == '4'){
      turns = right_step/2;
    }
    Photo_pressed1 = true;
    Photo_pressed2 = true;
    for(int i=0; i<turns; i++){
      Resistor1 = analogRead(A0);
      Resistor2 = analogRead(A1);
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
