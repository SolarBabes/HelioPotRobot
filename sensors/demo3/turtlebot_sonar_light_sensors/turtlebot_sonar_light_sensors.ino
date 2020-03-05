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

void setup() {
  
    sonar::Cluster front;
    sonar::Cluster back;
    
  // Set up pin numbers for FRONT cluster
    front.left.trig = 8;
    front.left.echo = 9;
    front.middle.trig = 4;
    front.middle.echo = 5;
    front.right.trig = 6;
    front.right.echo = 7;
    
  // Set up pin numbers for BACK cluster
    //back.left.trig = ;
    //back.left.echo = ;
    back.middle.trig = 2;
    back.middle.echo = 3;
    //back.right.trig = ;
    //back.right.echo = ;

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
    
    Serial.begin(9600); //REMEMBER TO CHANGE FOR ROS!!
}


long publishDistance(HC_SR04::Usound &sensor) { // CHANGE TO VOID FOR ROS
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
    //Get distances
    

}
