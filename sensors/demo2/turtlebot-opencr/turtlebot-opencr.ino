// ============================================================================
// SDP 2020 - DEMO 2
// GROUP 1  - SOLARBABES
// HELIOPOT
// ===============================================================================
// Code for showing that sensors give readings in a human-understandable way.
// !! 
//  The OpenCR board serial output is seen by the Rpi in its /dev
//  The OpenCR board can run Arduino code and has the same headers on top as Uno
// ===============================================================================

#include <SeeedOLED.h>
#include "DHT.h"
#include "Wire.h"

//==============
// PIN NUMBERS
//==============          // SENSOR
#define LIGHT_0_PIN  A0   // light sensor 0
#define LIGHT_1_PIN  A1   // light sensor 1
#define LIGHT_2_PIN  A2   // light sensor 2
#define LIGHT_3_PIN  A3   // light sensor 3
#define serialPi Serial

int lightVal[4]   = {0};
int avgLightCurrent = 0;
int currentMinLight = 0;
int currentMaxLight = 0;
int minLight = 0;
int maxLight = 0;


void setup() 
{
  Wire.begin();
  SeeedOled.init();  //initialze SEEED OLED display
  SeeedOled.clearDisplay();
  Serial.begin(9600);
  Serial.println("\n<--SERIAL READY-->\n");
  Wire.begin();
}

void loop() 
{    

  //PRINT LIVE READINGS
  Serial.println("LIVE READINGS");
  Serial.println("=============");
  // Print light readings
  //this sensor's 5V max is 1000lux!
  //so we map from 0-1023 raw to 0-1000 lux.
  lightVal[0] = analogRead(LIGHT_0_PIN);
  lightVal[1] = analogRead(LIGHT_1_PIN);
  lightVal[2] = analogRead(LIGHT_2_PIN);
  lightVal[3] = analogRead(LIGHT_3_PIN);
  for (int i=0; i<4; i++) {
    lightVal[i] = map(lightVal[i], 0, 1023, 0, 1000);

   //{"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}

    Serial.print("{\"sensor\":");
    Serial.print("\"LightSensor ");
    Serial.print(i);
    Serial.print("\"");
    Serial.print(",");
    Serial.print("\"time\":");
    Serial.print(millis());
    Serial.print(",");
    Serial.print("\"data\":");
    Serial.print(lightVal[i]);
    Serial.print("}");
    Serial.print("\n");

  }
  Serial.println();

  
  // Delay and newlines for readability
  Serial.println();
  Serial.println();
  Serial.println();
  delay(1000);

}
