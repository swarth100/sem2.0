#include <AccelStepper.h>

int GreenLed = 3;
int YellowLed = 2;
int Pin0 = 4; 
int Pin1 = 5; 
int Pin2 = 6; 
int Pin3 = 7; 
int Pin4 = 8; 
int Pin5 = 9; 
int Pin6 = 10; 
int Pin7 = 11; 
AccelStepper stepperBot(4, Pin0, Pin1, Pin2, Pin3);
AccelStepper stepperTop(4, Pin4, Pin5, Pin6, Pin7);
int Resistor1;
int Resistor2;
int Resistor3;
int Resistor4;
int turns = 0;
int right_step = 8600;
int left_step = 8600;
char command = ' ';
char input = ' ';
char verse = ' ';
boolean stepperBotSelected = false;
boolean stepperTopSelected = false;

void setup () {
  pinMode(GreenLed, OUTPUT);
  pinMode(YellowLed, OUTPUT);
  pinMode(Pin0, OUTPUT);  
  pinMode(Pin1, OUTPUT);  
  pinMode(Pin2, OUTPUT);  
  pinMode(Pin3, OUTPUT);
  Serial.begin (9600);
  stepperTop.setMaxSpeed(1000);
  stepperTop.setSpeed(180);
  stepperBot.setMaxSpeed(1000);
  stepperBot.setSpeed(180);
}

void loop (){
  stepperBotSelected = false;
  stepperTopSelected = false;
  stepperTop.setPinsInverted(false, false, false);
  stepperBot.setPinsInverted(false, true, false);
  digitalWrite(GreenLed, HIGH);
  digitalWrite(YellowLed, LOW);
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
    digitalWrite(GreenLed, LOW);
    digitalWrite(YellowLed, HIGH);
    //digitalWrite(LedPin, HIGH);
    if (command == '0'){
      stepperBotSelected = true; 
      turns = 10000;
    }
    if (command == '1'){
      stepperBotSelected = true;
      turns = right_step;
    }
    if (command == '2'){
      stepperTopSelected = true;
      turns = 10000;
    }
    if (command == '3'){
      stepperTopSelected = true;
      turns = left_step;
    }
    if (command == '4'){
      stepperBotSelected = true;
      turns = right_step/2;
    }
    if (command == '5'){
      stepperTopSelected = true;
      turns = left_step/2;
    }
    if (command == '6'){
      stepperBotSelected = true;
      stepperTopSelected = true;
      turns = left_step;
    }
    if (verse == '1'){
      if (stepperBotSelected){
          stepperBot.setPinsInverted(false, false, false);
        }
      if (stepperTopSelected){
          stepperTop.setPinsInverted(false, true, false);
        }
    }
    for(int i=0; i<turns; i++){
      if (stepperBotSelected){
        stepperBot.runSpeed();
      }
      if (stepperTopSelected){
        stepperTop.runSpeed();
      }
      delay (1);
      if ((i + 1) == turns){
        Serial.print('1');
        Serial.print('2');
        Serial.print(verse);
      }
    }
  digitalWrite(Pin0, LOW);
  digitalWrite(Pin1, LOW);
  digitalWrite(Pin2, LOW);
  digitalWrite(Pin3, LOW);
  digitalWrite(Pin4, LOW);
  digitalWrite(Pin5, LOW);
  digitalWrite(Pin6, LOW);
  digitalWrite(Pin7, LOW);
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
