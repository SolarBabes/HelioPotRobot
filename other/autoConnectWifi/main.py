import os
f = open("/home/pi/autowifi/info.txt","r")
content = f.read()

#0=wifi
#1=hotspot
hostapd0=""
hostapd1="""interface=wlan0
driver=nl80211
ssid=MyPiAP
hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=1
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=raspberry
rsn_pairwise=CCMP"""
dhcpcd0="""
hostname
clientid
persistent
option rapid_commit
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
option interface_mtu
require dhcp_server_identifier
slaac private
"""
dhcpcd1=dhcpcd0+"\ndenyinterfaces wlan0"


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
hostspd0=""
hostspd1='DAEMON_CONF="/etc/hostapd/hostapd.conf"'
interfaces0="source-directory /etc/network/interfaces.d"
interfaces1="""auto lo
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
dnsmasq0="""dhcp-mac=set:client_is_a_pi,B8:27:EB:*:*:*
dhcp-reply-delay=tag:client_is_a_pi,2
"""
dnsmasq1="""interface=wlan0
listen-address=192.168.5.1
bind-interfaces
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.5.100,192.168.5.200,24h
"""
command1=['systemctl enable hostapd','systemctl start hostapd','service dnsmasq start']
command0=['service dnsmasq stop','systemctl stop hostapd','systemctl disable hostapd']


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
    f = open("/etc/wpa_supplicant/wpa_supplicant.conf","a")
    wifiinfo = 'network={\nssid="'+ssid+'"\npsk="'+pw+'"\n}'
    print(wifiinfo)
    f.write("\n\n"+wifiinfo)

    f = open("/home/pi/autowifi/info.txt","w")
    f.write(wifiinfo)

    f = open("/etc/hostapd/hostapd.conf","w")
    f.write(hostapd0)

    f = open("/etc/dhcpcd.conf","w")
    f.write(dhcpcd0)

    f = open("/etc/default/hostapd","w")
    f.write(hostapd0)

    f = open("/etc/network/interfaces","w")
    f.write(interfaces0)

    f = open("/etc/dnsmasq.conf","w")
    f.write(dnsmasq0)

    for i in command0:
        os.system(i)
    os.system("reboot")
elif (len(content))==1:
    f = open("/etc/hostapd/hostapd.conf","w")
    f.write(hostapd1)

    f = open("/etc/dhcpcd.conf","w")
    f.write(dhcpcd1)

    f = open("/etc/default/hostapd","w")
    f.write(hostapd1)

    f = open("/etc/network/interfaces","w")
    f.write(interfaces1)

    f = open("/etc/dnsmasq.conf","w")
    f.write(dnsmasq1)

    for i in command1:
        os.system(i)
else:
    pass
  
