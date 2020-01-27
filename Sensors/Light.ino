#include <Grove_LED_Bar.h>
#include <Arduino.h>

void setup()
{
 	Serial.begin(9600);
 }

void loop()
{

  int value = analogRead(A0);
  
  Serial.println(value, DEC)
  delay(100);
}