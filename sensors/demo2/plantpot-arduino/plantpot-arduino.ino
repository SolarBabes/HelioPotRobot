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


// {"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}



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
  SeeedOled.init();
  SeeedOled.clearDisplay();
  Serial.begin(9600);
  Serial.println("\n<--SERIAL-READY-->\n");
  Wire.begin();
  dht.begin();

}

void loop() 
{   
 
  // {"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}
  
  // **OPEN SERIAL MESSAGE**
  Serial.println("{");
  
  // Print temp & humidity readings
  Serial.println("\"sensor:\":\"humidity\",\"time\" ");
  if(!dht.readTempAndHumidity(tempHumVal)) {
    
  } 
  else {
    Serial.println();
  }

  // Print moisture readings
  moistVal = analogRead(MOIST_PIN);
  Serial.print("Moisture: ");
  Serial.print(moistVal);
  if (0 <= moistVal && moistVal <150) {
    Serial.println(" ~ Very dry!");
  } 
  else if (150 <= moistVal && moistVal < 300) {
    Serial.println(" ~ Quite dry.");
  } 
  else if (300 <= moistVal && moistVal < 450) {
    Serial.println(" ~ A bit moist.");
  } 
  else if (450 <= moistVal && moistVal < 600) {
    Serial.println(" ~ Quite moist.");
  } 
  else if (600 <= moistVal && moistVal < 700) {
    Serial.println(" ~ Very moist!");
  } 
  else if (700 <= moistVal && moistVal < 825) {
    Serial.println(" ~ Very moist!");
  } 
  else if (825 <= moistVal && moistVal < 950) {
    Serial.println(" ~ Pretty much just water.");
  }
  Serial.println();



  //PRINT RUNNING MIN AND MAX
  /*
  Serial.println("RUNNING MIN AND MAX");
  if (tempHumVal[1] < minTemp) {
    minTemp = tempHumVal[1];
  }
  if (tempHumVal[0] < minHumid ) {
    minHumid = tempHumVal[0];
  }
  if (moistVal < minMoist) {
    minMoist = moistVal;
  }
*/

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
