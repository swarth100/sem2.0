int lightPin = A0;  //define a pin for Photo resistor
int ledPin=11;     //define a pin for LED

void setup()
{
    Serial.begin(9600);  //Begin serial communcation
}

void loop()
{
    Serial.println(analogRead(lightPin)); //Write the value of the photoresistor to the serial monitor.
    delay(100); //short delay for faster response to light.
    while (true){
      if (analogRead(lightPin) <= 500){
        Serial.print('0');
        break;
      }
    }
}
