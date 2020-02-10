
// ============================================================================
// SDP 2020 - DEMO 1
// GROUP 1  - SOLARBABES
// HELIOPOT
// ===============================================================================
// Code for showing that sensors give readings in a human-understandable way.
// !! 
// NOTE that the moisture sensor will be separated after demo 1, so that the 
//  separate Arduino for the plant will deal with moisture readings, and the
//  OpenCR board on the Turtlebot will deal with the humidity&temp (DHT) and
//  light sensor readings.
//  This means that this code is only functional for demo 1 and will need major
//  restructuring for demo 2 and onwards.
//  The OpenCR board serial output is seen by the Rpi in its /dev
//  The OpenCR board can run Arduino code and has the same headers on top as Uno
// ===============================================================================
// DHT portion originally written by ladyada, public domain
// Modified and extended by SolarBabes
// ===============================================================================
// Remember to connect the signal pin of the DHT sensor through a 10K resistor
//   to +5V!
// Also remember that the D in DHT stands for digital! The temp & humidity sensor
//   can be put in a digital pin!
// !! The current Uno we have has weird A4 and sometimes (??) A5 pins!!
//   If they don't work, try another pin.
// ===============================================================================

#include <SeeedOLED.h>
#include "DHT.h"
#include "Wire.h"

//==============
// PIN NUMBERS
//==============          // SENSOR                  // RIBBON COLOUR    
#define LIGHT_0_PIN  A0   // light sensor 0          // red
#define LIGHT_1_PIN  A1   // light sensor 1          // orange
#define LIGHT_2_PIN  A2   // light sensor 2          // yellow
#define LIGHT_3_PIN  A3   // light sensor 3          // green        // removed for demo 1!


int   lightVal[4]   = {0};
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
  //dht.begin();

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
    Serial.print("Light ");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(lightVal[i]);
    Serial.print(" lux\t\t"); 
  }
  Serial.println();


  //PRINT CURRENT AVG LIGHT
  Serial.println("CURRENT LIGHT AVERAGE");
  Serial.println("=====================");
  avgLightCurrent = (lightVal[0] + lightVal[1] + lightVal[2] + lightVal[3]) / 4;
  Serial.print(avgLightCurrent);
  Serial.println(" lux");
  

  // Delay and newlines for readability
  Serial.println();
  Serial.println();
  Serial.println();
  delay(1000);

}
