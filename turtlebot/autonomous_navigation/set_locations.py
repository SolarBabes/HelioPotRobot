import sys, socket, os, rospy, json
from nav_msgs.msg import Odometry

global coords, base_x, base_y, windows, locations

station_set = False
windows_counter = 0
locations = {}

# Create text file to store locations
folder = os.path.dirname(os.path.abspath(__file__))
text_file = os.path.join(folder, 'predefined_locations.txt')
text_file = open('predefined_locations.txt', 'w')
locations = {}
locations['charging_station'] = {}
locations['windows'] = {}

# text_file.write('charging_station:\n')
# text_file.write('windows_location:')
# locations = text_file.readlines()

# Socket for messages from the app
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('localhost', 8080))

# Get position
def odom_callback(msg):
    global coords
    coords = msg.pose.pose

def odom_listener():
    rospy.init_node('set_locations')
    rospy.Subscriber('/odom', Odometry, odom_callback)
    rospy.wait_for_message('/odom', Odometry, timeout=1)

# Receive message from button on the app
def get_message():
    msg = soc.recv(1024)
    msg = msg.decode('UTF-8')
    return msg


while(1):
    msg = (str(get_message())).rstrip()
    # Charging station can only be set once
    if (not(station_set) and msg == "charging_station"):
        odom_listener()
        # base_x = coords.position.x
        # base_y = coords.position.y
        # charging_station = '(' + str(base_x) + ',' + str(base_y) + ')'
        # locations[0] += charging_station
        # text_file.writelines(locations)
        locations['charging_station']['x'] = coords.position.x
        locations['charging_station']['y'] = coords.position.y
        station_set = True
    elif (msg == "window_location"):
        odom_listener()
        windows_counter += 1
        # windows.append((coords.position.x, coords.position.y))
        lcoations['windows'][windows_counter] = {}
        locations['windows'][windows_counter]['x'] = coords.position.x
        locations['windows'][windows_counter]['x'] = coords.position.y
    json.dump(locations, text_file)
        # locations[1] += windows
        # text_file.writelines(locations)

    # text_file.close()