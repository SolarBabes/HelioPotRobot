// IMPORTANT!!
//  Go to your Arduino libraries folder (usually home/Arduino/libraries,
//    or Documents/Arduino/libraries) and see what Grove_Sunlight_Sensor lib
//    you already have there.
//  If it is the multi2c_branch, delete/move it! If it is master, it's ok.
//  If you had the multi2c_branch one, follow the following steps:
//    1. Go to Sketch > Include Library > Add .ZIP Library... and add 
//          HelioPotRobot/sensors/lib/Grove_Sunlight_Sensor-master.zip
//    2. Close Arduino IDE and restart
// If the compiler throws an error when compiling you have done something wrong.

// Also, remember that whenever you want to do something with a certain sensor,
//  you MUST call tcaselect(x) where x is the number of the sensor.
// E.g. if you want to get a reading from sensor 0 then sensor 1, you must call
//  tcaselect(0) then read from sunS0, then call tcselect(1) then read from sunS1.

#include <Wire.h>
#include <SI114X.h>

#define TCAADDR 0x70

// Sunlight sensors 
SI114X sunS0 = SI114X();
SI114X sunS1 = SI114X();
SI114X sunS2 = SI114X();
SI114X sunS3 = SI114X();

// Sunlight averages
int avgVis, avgIR;
float avgUV;

// Phidgets light sensors
int lightPin0 = A0;
int lightPin1 = A1;
int lightPin2 = A2;
int lightPin3 = A3;

int lightVal[4];
int avgLightCurrent = 0;


// #############
//   FUNCTIONS
// #############

void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}


void printSunlightReadings(SI114X *sensor, int &Vis, int &IR, float &UV) {
  
  Vis = sensor->ReadVisible();
  Serial.print("\tVis:\t"); Serial.println(Vis);

  IR = sensor->ReadIR();
  Serial.print("\tIR:\t"); Serial.println(IR);

  UV = (float) sensor->ReadUV() / 100;
  Serial.print("\tUV:\t"); Serial.println(UV);

  avgVis += Vis;
  avgIR  += IR;
  avgUV  += UV;
  
}



// ###########
//   SETUP
// ###########

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Serial.println("<--- SERIAL READY --->");

  // initialise sensor 0
  tcaselect(0);
  while (!sunS0.Begin()) {
    Serial.println("There was a problem connecting to sensor 0");
    delay(1000);
  }

  // initialise sensor 1
  tcaselect(1);
  while (!sunS1.Begin()) {
    Serial.println("There was a problem connecting to sensor 1");
    delay(1000);
  }

  // initialise sensor 2
  tcaselect(2);
  while (!sunS2.Begin()) {
    Serial.println("There was a problem connecting to sensor 2");
    delay(1000);
  }

  // initialise sensor 3
  tcaselect(3);
  while (!sunS3.Begin()) {
    Serial.println("There was a problem connecting to sensor 3");
    delay(1000);
  }
  

}


// ###########
//    LOOP
// ###########

void loop() {
  
  // Get sunlight readings
  Serial.println("SUNLIGHT SENSOR READINGS");
  Serial.println("========================");
  int Vis = 0;
  int IR = 0;
  float UV = 0;

  tcaselect(0);
  printSunlightReadings(&sunS0, Vis, IR, UV);
  Serial.println();

  tcaselect(1);
  printSunlightReadings(&sunS1, Vis, IR, UV);
  Serial.println();

  tcaselect(2);
  printSunlightReadings(&sunS2, Vis, IR, UV);
  Serial.println();

  tcaselect(3);
  printSunlightReadings(&sunS3, Vis, IR, UV);
  Serial.println();

  // get average
  avgVis /= 4;
  avgIR /= 4;
  avgUV /= 4;
  Serial.println("Current sunlight averages:");
  Serial.print("\tavgVis:\t"); Serial.println(avgVis);
  Serial.print("\tavgIR:\t");  Serial.println(avgIR);
  Serial.print("\tavgUV:\t");  Serial.println(avgUV);
  Serial.println();
  Serial.println();
  
  // reset globals to 0 lol
  avgVis = 0;
  avgIR  = 0;
  avgUV  = 0;


  // Get Phidgets light sensor readings
  Serial.println("PHIDGETS LIGHT SENSOR READINGS");
  Serial.println("==============================");
  lightVal[0] = analogRead(lightPin0);
  lightVal[1] = analogRead(lightPin1);
  lightVal[2] = analogRead(lightPin2);
  lightVal[3] = analogRead(lightPin3);
  for (int i=0; i<4; i++) {
    lightVal[i] = map(lightVal[i], 0, 1023, 0, 1000);
    Serial.print("Light ");
    Serial.print(i);
    Serial.print(": ");
    Serial.print(lightVal[i]);
    Serial.print(" lux\t\t"); 
  }
  Serial.println();
  Serial.print("Phidgets current light average:\n\t");
  avgLightCurrent = (lightVal[0] + lightVal[1] + lightVal[2] + lightVal[3]) / 4;
  Serial.print(avgLightCurrent);
  Serial.println(" lux");
  Serial.println();
  Serial.println();

  delay(2000);
  

}
