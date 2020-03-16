# 1) run ./create_map.sh, create the map (using teleop) and save it
# 2) Quit ./create_map.sh, launch ./navigation.sh
# 3) Run this script to get the initial configuration of the robot,
#    and publish it to the navigation node.

rostopic echo /odom -n1 > initial_position.txt
python get_initial_position.py