f = open("info.txt","r")
content = f.read()

hotspot="""
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.5.1
    netmask 255.255.255.0
    network 192.168.5.0
    broadcast 192.168.5.255
"""
wifi = "source-directory /etc/network/interfaces.d"

def receive():
    import socket
    ip="192.168.5.1"
    port=8765
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip,port))
    d1,a1=sock.recvfrom(1024)
    print(d1)
    print(a1)
    sock.sendto(str.encode("ssid received"),a1)
    d2,a2=sock.recvfrom(1024)
    print(d2)
    sock.sendto(str.encode("password received"),a2)
    return(str(d1,"utf-8"),str(d2,"utf-8")) 
    
print(content)
if (len(content))==0:
    ssid,pw = receive()
    f1 = open("/etc/wpa_supplicant/wpa_supplicant.conf","a")
    wifiinfo = 'network={\nssid="'+ssid+'"\nkey_mgmt="'+pw+'"\n}'
    f1.write("\n\n"+wifiinfo)
    f2 = open("/etc/network/interfaces","w")
    f2.write(wifi)


