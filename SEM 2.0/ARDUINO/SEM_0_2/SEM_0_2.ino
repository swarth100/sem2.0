#include <AccelStepper.h>

int GreenLed = 3;
int EMPin = 2;
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
int right_step = 8700;
int left_step = 8700;
char verse_y = ' ';
char command = ' ';
char verse_x = ' ';
boolean stepperBotSelected = false;
boolean stepperTopSelected = false;

void setup () {
  pinMode(GreenLed, OUTPUT);
  pinMode(Pin0, OUTPUT);  
  pinMode(Pin1, OUTPUT);  
  pinMode(Pin2, OUTPUT);  
  pinMode(Pin3, OUTPUT);
  pinMode(EMPin, OUTPUT);
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
  if (Serial.available()>=3){
    command = Serial.read();
    verse_x = Serial.read();
    verse_y = Serial.read();
    Serial.print('1');
  }
  if (command == '2'){
    stepperBotSelected = true;
    turns = right_step;
  }
  if (command == '6'){
    stepperTopSelected = true;
    turns = left_step;
  }
  if (command == '1'){
    stepperBotSelected = true;
    turns = right_step/6;
  }
  if (command == '3'){
    stepperTopSelected = true;
    turns = left_step/6;
  }
  if (command == '8'){
    stepperBotSelected = true;
    stepperTopSelected = true;
     turns = left_step;
  }
  if (command == '4'){
    stepperBotSelected = true;
    stepperTopSelected = true;
     turns = left_step/2;
  }
  if (command == '7'){
    digitalWrite(EMPin, LOW);
    turns = 0;
  }
  if (command == '5'){
    digitalWrite(EMPin, HIGH);
    turns = 0;
  }
  if (verse_x == '1'){
    if (stepperBotSelected){
        stepperBot.setPinsInverted(false, false, false);
      }
  }
  if (verse_y == '1'){
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
  }
  digitalWrite(Pin0, LOW);
  digitalWrite(Pin1, LOW);
  digitalWrite(Pin2, LOW);
  digitalWrite(Pin3, LOW);
  digitalWrite(Pin4, LOW);
  digitalWrite(Pin5, LOW);
  digitalWrite(Pin6, LOW);
  digitalWrite(Pin7, LOW);
  verse_x = ' ';
  command = ' ';
  verse_y = ' ';
}
