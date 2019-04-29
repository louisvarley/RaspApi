from threading import Thread
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from myRaspPI.utils import logging
import myRaspPI
import platform

class Discovery():
       MAGIC = "myRaspPI"
       PORT = 50000

class Monitor(Thread):

    def __init__(self):
        logging.loggingService.logInfo(" * Starting Discovery Monitor Service")
        Thread.__init__(self)

    def run(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', Discovery.PORT))

        while 1:
            data, addr = s.recvfrom(1024) #wait for a packet
            ip= gethostbyname(gethostname()) 
            if data.startswith(Discovery.MAGIC.encode()) and data[len(Discovery.MAGIC):].decode() != ip+":"+str(myRaspPI.port)+":"+ str(platform.uname()[1]):
                print("got service announcement from " + data[len(Discovery.MAGIC):].decode())
 
class Broadcast(Thread):

    def __init__(self):
        logging.loggingService.logInfo(" * Starting Discovery Broadcast Service")
        Thread.__init__(self)

    def run(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
        ip= gethostbyname(gethostname()) 

        while 1:
            data = Discovery.MAGIC+ip+":"+str(myRaspPI.port) + ":" + str(platform.uname()[1])
            s.sendto(data.encode(),('<broadcast>', Discovery.PORT))
            sleep(5)       
            
   



