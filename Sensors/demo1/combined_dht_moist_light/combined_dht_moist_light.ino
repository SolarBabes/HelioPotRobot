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

#include "DHT.h"
#include "Wire.h"

//==============
// PIN NUMBERS
//==============
#define LIGHT_0_PIN  A0   // light sensor 0
#define LIGHT_1_PIN  A1   // light sensor 1
#define LIGHT_2_PIN  A2   // light sensor 2
#define LIGHT_3_PIN  A3   // light sensor 3
#define DHT_PIN      4    // temperature and humidity sensor
#define MOIST_PIN    A5   // moisture sensor

#define DHTTYPE DHT11   // DHT 11
DHT dht(DHT_PIN, DHTTYPE);

int   light0Val     = 0;
int   light1Val     = 0;
int   light2Val     = 0;
int   light3Val     = 0;
float tempHumVal[2] = {0}; 
int   moistVal       = 0;

void setup() 
{
    Serial.begin(9600);
    Serial.println("DHT11 test!");
    Wire.begin();
    dht.begin();
}

void loop() 
{    
    // Print light readings
    light0Val = analogRead(LIGHT_0_PIN);
    //this sensor's 5V max is 1000lux!
    //so we map from 0-1023 raw to 0-1000 lux.
    light0Val = map(light0Val, 0, 1023, 0, 1000);
    Serial.print("Light: ");
    Serial.print(light0Val, DEC);
    Serial.println(" lux");
    
    // Print temp & humidity readings
    if(!dht.readTempAndHumidity(tempHumVal)) {
        Serial.print("Humidity: "); 
        Serial.print(tempHumVal[0]);
        Serial.print(" %\t");
        Serial.print("Temperature: "); 
        Serial.print(tempHumVal[1]);
        Serial.println(" *C");
    } else {
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
    } else if (150 <= moistVal && moistVal < 300) {
      Serial.println(" ~ Quite dry.");
    } else if (300 <= moistVal && moistVal < 450) {
      Serial.println(" ~ A bit moist.");
    } else if (450 <= moistVal && moistVal < 600) {
      Serial.println(" ~ Quite moist.");
    } else if (600 <= moistVal && moistVal < 700) {
      Serial.println(" ~ Very moist!");
    } else if (700 <= moistVal && moistVal < 825) {
      Serial.println(" ~ Very moist!");
    } else if (825 <= moistVal && moistVal < 950) {
      Serial.println(" ~ Pretty much just water.");
    }

    // Delay and newline for readability
    Serial.println();
    delay(1000);
   
}
