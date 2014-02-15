import socket
import datetime

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    ''' print "received message at :" + datetime.datetime.now().time().isoformat() + ": " + data '''
    print data
    sock.sendto("hello back from server!", addr)