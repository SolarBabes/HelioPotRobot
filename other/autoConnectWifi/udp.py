import socket
ip="192.168.5.1"
port=8765
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((ip,port))

d,a=sock.recvfrom(1024)
print(str(d,"utf-8")+'1')
sock.sendto(str.encode("ssid received"),a)
d,a=sock.recvfrom(1024)
print(d)
sock.sendto(str.encode("password received"),a)
    
