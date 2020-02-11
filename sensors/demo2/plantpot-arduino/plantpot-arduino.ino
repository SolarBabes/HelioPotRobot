// ============================================================================
// SDP 2020 - DEMO 2
// GROUP 1  - SOLARBABES
// HELIOPOT
// ===============================================================================
// Code for sending data from the ** Arduino Uno **, via USB, to the Turtlebot RPi
//  The OpenCR board serial output is seen by the Rpi in its /mnt/
//  The OpenCR board can run Arduino code and has the same headers on top as Uno
// ===============================================================================
// DHT portion originally written by ladyada, public domain
// Modified and extended by SolarBabes
// ===============================================================================
// Remember that the D in DHT stands for digital! The temp & humidity sensor
//   can be put in a digital pin!
// ===============================================================================


#include <SeeedOLED.h>
#include "DHT.h"
#include "Wire.h"



//==============
// PIN NUMBERS
//==============          // SENSOR                      
#define DHT_PIN      8    // temp & humidity sensor  
#define MOIST_PIN    A0   // moisture sensor         

#define DHTTYPE DHT11     // DHT 11
DHT dht(DHT_PIN, DHTTYPE);


float tempHumVal[2] = {0}; 
int moistVal = 0;
int minTemp  = 0;
int minHumid = 0;
int minMoist = 0;
int maxTemp  = 0;
int maxHumid = 0;
int maxMoist = 0;

void setup() 
{
  Wire.begin();
  SeeedOled.init();
  SeeedOled.clearDisplay();
  Serial.begin(9600);
  Serial.println("\n<--SERIAL-READY-->\n");
  Wire.begin();
  dht.begin();

}

void loop() 
{   
  
  // **OPEN SERIAL MESSAGE**
  
  // Print temp & humidity readings
  //Serial.println("\"sensor:\":\"humidity\",\"time\" ");
  if(!dht.readTempAndHumidity(tempHumVal)) {

    Serial.print("{\"sensor\":");
    Serial.print("\"temperature");
    Serial.print("\"");
    Serial.print(",");
    Serial.print("\"time\":");
    Serial.print(millis());
    Serial.print(",");
    Serial.print("\"data\":");
    Serial.print(tempHumVal[1]);
    Serial.print("}");
    Serial.print("\n");
    Serial.print("{\"sensor\":");
    Serial.print("\"humidity");
    Serial.print("\"");
    Serial.print(",");
    Serial.print("\"time\":");
    Serial.print(millis());
    Serial.print(",");
    Serial.print("\"data\":");
    Serial.print(tempHumVal[0]);
    Serial.print("}");
    Serial.print("\n");
    
  } 
  else {
    Serial.println();
  }

  // Print moisture readings
  moistVal = analogRead(MOIST_PIN);
  //Serial.print("Moisture: ");
  //Serial.print(moistVal);

    Serial.print("{\"sensor\":");
    Serial.print("\"moisture");
    Serial.print("\"");
    Serial.print(",");
    Serial.print("\"time\":");
    Serial.print(millis());
    Serial.print(",");
    Serial.print("\"data\":");
    Serial.print(moistVal);
    Serial.print("}");
    Serial.print("\n");



  Serial.println();





  //PRINT TO OLED DISPLAY
  SeeedOled.setTextXY(1, 0);
  SeeedOled.putString("\n");
  SeeedOled.putString("Temp: ");
  SeeedOled.putNumber(tempHumVal[1]); //Print the String
  SeeedOled.putString("\tC");
  
  SeeedOled.setTextXY(2, -1);
  SeeedOled.putString("\n");
  SeeedOled.putString("Humid: ");
  SeeedOled.putNumber(tempHumVal[0]); //Print the String
  SeeedOled.putString("\t%");
  
  SeeedOled.setTextXY(3, -1);
  SeeedOled.putString("\n");
  SeeedOled.putString("Moist: ");
  SeeedOled.putNumber(moistVal); //Print the String
  SeeedOled.putString("    ");
  

  // Delay and newlines for readability
  Serial.println();
  Serial.println();
  Serial.println();
  delay(1000);

}
