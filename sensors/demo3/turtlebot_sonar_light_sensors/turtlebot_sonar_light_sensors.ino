// If this is your first time running this sketch, make sure to do the following:
// Sketch -> Include library -> Add .ZIP library...
//  for HelioPotRobot/sensors/lib
//                               /Arduino_Software_I2C-master.zip
//                               /Arduino_Software_I2C-softi2c_branch.zip
//                               /Grove_Sunlight_Sensor-master.zip

// sunlight sensors' I2C address is 0x60


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

// Sunlight sensors in shield I2C port
SI114X sunS0         = SI114X();          // real I2C     SDA-SCL   (Grove I2C)



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
    
    while (!sunS0.Begin()) {
      Serial.println("sunS0 not ready...");
      delay(1000);
    }

    
    Serial.println("sunlight sensors are ready! (?)");
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
    Serial.println("S0:");
      Serial.print("\tVis:\t"); Serial.println(sunS0.ReadVisible());
      Serial.print("\tIR:\t"); Serial.println(sunS0.ReadIR());
      Serial.print("\tUV:\t");  Serial.println((float)sunS0.ReadUV()/100); // see datasheet for div 100
//    Serial.println("S1:");
//      Serial.print("\tVis:\t"); Serial.println(sunS1.ReadVisible());
//     Serial.print("\tIR:\t"); Serial.println(sunS1.ReadIR());
//      Serial.print("\tUV:\t");  Serial.println((float)sunS1.ReadUV()/100); // see datasheet for div 100
//    Serial.println("S2:");
//      Serial.print("\tVis:\t"); Serial.println(sunS2.ReadVisible());
//      Serial.print("\tIR:\t"); Serial.println(sunS2.ReadIR());
//      Serial.print("\tUV:\t");  Serial.println((float)sunS2.ReadUV()/100); // see datasheet for div 100
//    Serial.println("S3:");
//      Serial.print("\tVis:\t"); Serial.println(sunS3.ReadVisible());
//      Serial.print("\tIR:\t"); Serial.println(sunS3.ReadIR());
//      Serial.print("\tUV:\t");  Serial.println((float)sunS3.ReadUV()/100); // see datasheet for div 100

    // Delay and newlines for readability
    Serial.println();
    Serial.println();
    Serial.println();
    delay(1000);
  }
