#include <SI114X.h>
#include <SI114X_softi2c.h>
#include <SoftwareI2C.h>
#include <Wire.h>

//ROS THINGS
/*
#include <ros.h>
#include <std_msgs/Float64.h>
ros::NodeHandle nh;
std_msgs::Float64 Distance;
ros::Publisher chatter("chatter",&Distance);
 */

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

sonar::Cluster front;
sonar::Cluster back;

// Sunlight sensor in shield I2C port
SI114X SI1145 = SI114X();


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
    while (!SI1145.Begin()) {
      Serial.println("Si1145 is not ready!");
      delay(1000);
    }
    Serial.println("Si1145 is ready!");
}


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
 
void loop() {
    //Get distances and print em
    Serial.println("SONAR READINGS");
    Serial.println("=============");
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
    Serial.print("Vis: "); Serial.println(SI1145.ReadVisible());
    Serial.print("IR: "); Serial.println(SI1145.ReadIR());
    //the real UV value must be div 100 from the reg value , datasheet for more information.
    Serial.print("UV: ");  Serial.println((float)SI1145.ReadUV()/100);

    // Delay and newlines for readability
    Serial.println();
    Serial.println();
    Serial.println();
    delay(1000);
  }
