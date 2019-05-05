from threading import Thread
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from myRaspPI.core import logging
import myRaspPI
import platform

from urllib.request import urlopen

class Discovery():
    magicPrefix = "myRaspPI"
    magicPort = 50000
    magicIP = gethostbyname(gethostname()) 
    magicClientString = magicPrefix + magicIP+":"+str(myRaspPI.config.port)+":"+ str(platform.uname()[1].upper())

class Client():

    def __init__(self,ipAddress,port,hostName):
        self.hostName = hostName
        self.ipAddress = ipAddress
        self.port = port
        self.loaded = False
        self.apiSpec = "http://" + self.ipAddress + ":" + self.port + "/spec.json"

class Clients():

    def __init__(self):
        self.clientList = {}

    def newClient(self,client):
        self.clientList.update({client.ipAddress:client})

    def clientFromClientString(self,clientString):
        if(":" in clientString):
            cData = clientString.split(":")
            i = Client(cData[0],cData[1],cData[2])
            return i
        else:
            return False

    def isClient(self,ipAddress):
        if ipAddress in self.clientList:
            return True
        else:
            return False

    def isClientOnline(self,ipAddress):
        if ipAddress in self.clientList:
            return True
        else:
            return False

    def listClients():
        return self.clientList

class DiscoveryMonitor(Thread):

    def __init__(self):
        logging.loggingService.logInfo(" * Starting Discovery Monitor Service")
       

        Thread.__init__(self)

    def run(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', Discovery.magicPort))

        self.clients = Clients()

        while 1:
            data, addr = s.recvfrom(1024) #wait for a packet
            
            #Check if is discovery magic string and isnt this client
            if data.decode().startswith(Discovery.magicPrefix) and data.decode() != Discovery.magicClientString:
                clientString = data[len(Discovery.magicPrefix):].decode()
                #Isnt already added to the clients list
                if self.clients.isClient(self.clients.clientFromClientString(clientString).ipAddress) == False:
                    client = self.clients.clientFromClientString(clientString)                 
                    self.clients.newClient(client)
                    
 
class DiscoveryBroadcast(Thread):

    def __init__(self):
        logging.loggingService.logInfo(" * Starting Discovery Broadcast Service")
        Thread.__init__(self)

    def run(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
        ip= gethostbyname(gethostname()) 

        while 1:
            data = Discovery.magicClientString
            s.sendto(data.encode(),('<broadcast>', Discovery.magicPort))
            sleep(5)       
            
   



