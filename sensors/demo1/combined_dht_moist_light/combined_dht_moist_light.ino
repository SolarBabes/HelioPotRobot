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
//#define LIGHT_3_PIN  A5   // light sensor 3          // green        // removed for demo 1!
#define DHT_PIN      4    // temp & humidity sensor  // blue
#define MOIST_PIN    A3   // moisture sensor         // purple      //<-- this boy likes to draw a whole lot of current

#define DHTTYPE DHT11   // DHT 11
DHT dht(DHT_PIN, DHTTYPE);

int   lightVal[3]   = {0};
float tempHumVal[2] = {0}; 
int   moistVal      = 0;
int avgLightCurrent = 0;
int currentMinLight = 0;
int currentMaxLight = 0;
int minLight = 0;
int minTemp  = 0;
int minHumid = 0;
int minMoist = 0;
int maxLight = 0;
int maxTemp  = 0;
int maxHumid = 0;
int maxMoist = 0;

void setup() 
{
  Wire.begin();
  SeeedOled.init();  //initialze SEEED OLED display
  SeeedOled.clearDisplay();
  Serial.begin(9600);
  Serial.println("\n<--SERIAL READY-->\n");
  Wire.begin();
  dht.begin();

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
//  lightVal[3] = analogRead(LIGHT_3_PIN);
  for (int i=0; i<3; i++) {
    lightVal[i] = map(lightVal[i], 0, 1023, 0, 1000);
    Serial.print("Light ");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(lightVal[i]);
    Serial.print(" lux\t\t"); 
  }
  Serial.println();

  // Print temp & humidity readings
  if(!dht.readTempAndHumidity(tempHumVal)) {
    Serial.print("Humidity: "); 
    Serial.print(tempHumVal[0]);
    Serial.print(" %\t");
    Serial.print("Temperature: "); 
    Serial.print(tempHumVal[1]);
    Serial.println(" *C");
  } 
  else {
    Serial.println("Failed to get temperature and humidity value.");
  }

  // Print moisture readings
  //   Reading temperature or humidity takes about 250 milliseconds!
  //   Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  //  "It is just a value reflect the humidity of soil.We do not standardization.Regards." -Grove FAQ admin
  //     0-300 dry soil
  //   300-700 humid soil
  //   700-950 water
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

  //PRINT CURRENT AVG LIGHT
  Serial.println("CURRENT LIGHT AVERAGE");
  Serial.println("=====================");
  avgLightCurrent = (lightVal[0] + lightVal[1] + lightVal[2]/* + lightVal[3]*/) / 3;
  Serial.print(avgLightCurrent);
  Serial.println(" lux");


  //PRINT RUNNING MIN AND MAX
  /*
  Serial.println("RUNNING MIN AND MAX");
  Serial.println("===================");
  currentMinLight = min(lightVal[0], min(lightVal[1], min(lightVal[2], lightVal[3])));
  currentMaxLight = max(lightVal[0], max(lightVal[1], max(lightVal[2], lightVal[3])));
  
  if (currentMinLight < minLight) {
    minLight = currentMinLight;
  }
  Serial.print("Minimum light: ");
  Serial.println(minLight);
  if (currentMaxLight < maxLight) {
    maxLight = currentMaxLight;
  }
  
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
  SeeedOled.setNormalDisplay();      //Set display to normal mode (i.e non-inverse mode)
  SeeedOled.setPageMode();           //Set addressing mode to Page Mode
  SeeedOled.setTextXY(0, 0);         //Set the cursor to Xth Page, Yth Column
  SeeedOled.putString("Light: ");
  SeeedOled.putNumber(avgLightCurrent); //Print the String
  SeeedOled.putString("\tlux ");

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

