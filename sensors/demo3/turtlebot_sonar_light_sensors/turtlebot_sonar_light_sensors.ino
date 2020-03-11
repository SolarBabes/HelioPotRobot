// If this is your first time running this sketch, make sure to do the following:
// Sketch -> Include library -> Add .ZIP library...
//  for HelioPotRobot/sensors/lib
//                               /Arduino_Software_I2C-multi2c_branch.zip
//                               /Grove_Sunlight_Sensor-master.zip


// sensor sunS1 : 0x10
// sensor sunS2 : 0x20
// sensor sunS3 : 0x30
// sensor sunS4 : 0x40


// READ THE BELOW INSTRUCTIONS CAREFULLY!!

// 0. Find the three lines in setup() with the commented arrows pointing at them.
//      Remember these - they are the lines where you need to change variables
//      each time you set up each sensor.

// 1. Plug ONE sunlight sensor into the Arduino. This will be sensor 1 (sunS1).
// 2. Ensure that the three lines in setup() are referring to sunS1 and 0x10.   
//      (of course, only the object reference and numerical value parameters have an actual
//       effect, but if you also change the printed lines accordingly you will save yourself
//       a lot of grief) 
// 3. Upload the sketch, open the serial monitor and confirm that the address change
//      has happened.
// 4. Close the serial monitor, add the next sensor to the board (don't touch any
//      previously set up sensor!)
// 5. Repeat these steps, changing the variables in the three lines in setup() according
//      to what sensor you are setting up.

// If you have done all of this successfully, all four sensors should be printing sensible
//      sunlight readings together in the serial monitor!



// IF YOU UNPLUG ANY SENSOR OR THE ARDUINO USB AT ANY POINT, YOU NEED TO START FROM THE BEGINNING
//    AND DO IT ALL AGAIN!!


//#######################
// INCLUDES
//#######################

#include <SI114X.h>
#include <Wire.h>


//#######################
// ROS THINGS
//#######################
/*
#include <ros.h>
#include <std_msgs/Float64.h>
ros::NodeHandle nh;
std_msgs::Float64 Distance;
ros::Publisher chatter("chatter",&Distance);
 */


//#######################
// GLOBALS
//#######################

namespace HC_SR04 {
  typedef struct {
    int trig;
    int echo;
  } Usound;
}

namespace sonar {
  typedef struct {
    HC_SR04::Usound left;
    HC_SR04::Usound middle;
    HC_SR04::Usound right;
  } Cluster;
}

long duration;
float distance;
char chr_dist[4];


// Ultrasound sensors
sonar::Cluster front;
sonar::Cluster back;

// Sunlight sensors in shield I2C ports
SI114X sunS1 = SI114X(0x10);
SI114X sunS2 = SI114X(0x20);
SI114X sunS3 = SI114X(0x30);
SI114X sunS4 = SI114X(0x40);

uint8_t confirmAddress;
bool sunSensorConfirm = true;

//#######################
// SETUP
//#######################

void setup() {
    
  // Set up pin numbers for FRONT cluster
    front.left.trig = 8;
    front.left.echo = 9;
    front.middle.trig = 4;
    front.middle.echo = 5;
    front.right.trig = 6;
    front.right.echo = 7;
    
  // Set up pin numbers for BACK cluster
    back.left.trig = 12;
    back.left.echo = 13;
    back.middle.trig = 2;
    back.middle.echo = 3;
    back.right.trig = 10;
    back.right.echo = 11;

  // Set up pin modes
    pinMode(front.left.trig, OUTPUT);
    pinMode(front.left.echo, INPUT);
    pinMode(front.middle.trig, OUTPUT);
    pinMode(front.middle.echo, INPUT);
    pinMode(front.right.trig, OUTPUT);
    pinMode(front.right.echo, INPUT);
    pinMode(back.left.trig, OUTPUT);
    pinMode(back.left.echo, INPUT);
    pinMode(back.middle.trig, OUTPUT);
    pinMode(back.middle.echo, INPUT);
    pinMode(back.right.trig, OUTPUT);
    pinMode(back.right.echo, INPUT);
    
    Serial.begin(115200); //REMEMBER TO CHANGE FOR ROS!!
    Serial.println("\n<--SERIAL READY-->\n");

    Serial.println("Setting up sunS4 with address 0x40...");   // <----------  CHANGE EACH TIME YOU RUN! SEE TOP OF FILE
    confirmAddress = setUpSunlightSensor(&sunS4, 0x40);        // <----------  CHANGE EACH TIME YOU RUN! SEE TOP OF FILE
    Serial.print("sunS4 address is now ");                     // <----------  CHANGE EACH TIME YOU RUN! SEE TOP OF FILE
    Serial.println(confirmAddress);
    Serial.println();
    
}


//#######################
// FUNCTIONS
//#######################

void publishDistance(HC_SR04::Usound &sensor) { // CHANGE TO VOID FOR ROS
  // Clear trig pin
  digitalWrite(sensor.trig, LOW);
  delayMicroseconds(2);
  
  // Set trig pin high for 10mics
  digitalWrite(sensor.trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(sensor.trig, LOW);
  
  // Read echo pin, calculate distance
  duration = pulseIn(sensor.echo, HIGH);
  distance = duration * 0.034/2;
  
// ROS PUBLISH CODE
/*
Distance.data = distance;
chatter.publish(&Distance);
nh.spinOnce(); 
 */

//Print to serial monitor
  Serial.print("Distance: ");
  Serial.println(distance);
  delay(100);
}


uint8_t setUpSunlightSensor(SI114X *sensor, uint8_t newAddr) {
  // if sensor responds to default addr...change its addr
  if (sensor->Begin(0x60)) {
    sensor->SetNewSlaveAddress(0x60, newAddr);
  // otherwise it should already be listening to its newAddr
  //  ...but it could still have a bad internal addr of 255, so reset and fix that
  } else if (sensor->Begin(newAddr)) {
    if (sensor->ReadParamData(newAddr, 0x00) == 255) {
      sensor->Reset(0xFF);
      sensor->Begin(0x60);
      sunS1.SetNewSlaveAddress(0x60, newAddr);
    }
  }
  
  return sensor->ReadParamData(newAddr, 0x00);
}


//#######################
// LOOP
//#######################

void loop() {
    //Get distances and print em
    Serial.println("SONAR READINGS");
    Serial.println("==============");
    Serial.println("FRONT");
    Serial.print("\tleft:\t");
    publishDistance(front.left);
    Serial.print("\tmiddle:\t");
    publishDistance(front.middle);
    Serial.print("\tright:\t");
    publishDistance(front.right);
    Serial.println();
    Serial.println("BACK");
    Serial.print("\tright:\t");
    publishDistance(back.right);
    Serial.print("\tmiddle:\t");
    publishDistance(back.middle);
    Serial.print("\tleft:\t");
    publishDistance(back.left);
    Serial.println();
    Serial.println();
    Serial.println();


    //Get light readings
    Serial.println("SUNLIGHT SENSOR READINGS");
    Serial.println("========================");
    Serial.println("S1:");
      Serial.print("\tVis:\t"); Serial.println(sunS1.ReadVisible());
      Serial.print("\tIR:\t"); Serial.println(sunS1.ReadIR());
      Serial.print("\tUV:\t");  Serial.println((float)sunS1.ReadUV()/100); // see datasheet for div 100
    Serial.println("S2:");
      Serial.print("\tVis:\t"); Serial.println(sunS2.ReadVisible());
      Serial.print("\tIR:\t"); Serial.println(sunS2.ReadIR());
      Serial.print("\tUV:\t");  Serial.println((float)sunS2.ReadUV()/100); // see datasheet for div 100
    Serial.println("S3:");
      Serial.print("\tVis:\t"); Serial.println(sunS3.ReadVisible());
      Serial.print("\tIR:\t"); Serial.println(sunS3.ReadIR());
      Serial.print("\tUV:\t");  Serial.println((float)sunS3.ReadUV()/100); // see datasheet for div 100
    Serial.println("S4:");
      Serial.print("\tVis:\t"); Serial.println(sunS4.ReadVisible());
      Serial.print("\tIR:\t"); Serial.println(sunS4.ReadIR());
      Serial.print("\tUV:\t");  Serial.println((float)sunS4.ReadUV()/100); // see datasheet for div 100

    // Delay and newlines for readability
    Serial.println();
    Serial.println();
    Serial.println();
    delay(3000);
  }
