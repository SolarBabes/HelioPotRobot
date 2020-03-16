coords=$(python generate_pubstring.py)
rostopic pub /initialpose geometry_msgs/PoseWithCovarianceStamped "$coords"
