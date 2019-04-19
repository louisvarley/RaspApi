from flask import Flask, jsonify, redirect
from flasgger import Swagger
from flasgger.utils import swag_from
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname

import urllib
import json 
import ssl
import scapy.all as scapy
import argparse
import threading

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

app.config['SWAGGER'] = {
  'title': 'RaspApi',
  'uiversion': 2
}

swagger = Swagger(app)


class ServiceFinder(threading.Thread):

    def broadcast(self):
        PORT = 50000
        MAGIC = "RaspiApi" #to make sure we don't confuse or get confused by other programs 
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #this is a broadcast socket
        ip= gethostbyname(gethostname()) #get our IP. Be careful if you have multiple network interfaces or IPs

        while 1:
            data = MAGIC+ip
            s.sendto(data, ('<broadcast>', PORT))
            sleep(5)       
            
    def discovery(self):
        s = socket(AF_INET, SOCK_DGRAM) #create UDP socket
        s.bind(('', PORT))

        while 1:
            data, addr = s.recvfrom(1024) #wait for a packet
            if data.startswith(MAGIC):
                print "got service announcement from", data[len(MAGIC):]
 


 
#Load the Given Path and Swag from a remote instance */
def loadRemoteSwagResource(path,swag):
        exec("""
@app.route('""" + str(path) + """')
@swag_from(""" + str(data['paths'][path]) + """)
def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
    return {'response':'response'}
        """)  

#Redirect Root to Swagger Docs        
@app.route('/')
def root():
 return redirect("/apidocs/", code=302)




url = urllib.urlopen("https://my-landscape-inst-api-uat.azurewebsites.net/swagger/docs/v1")
data = json.loads(url.read().decode())

for path in data['paths']:
    loadRemoteSwagResource(str(path),str(data['paths'][path]))
       
if __name__ == '__main__':       
    broadcast()
    discovery()
    
    discovery = threading.Thread(target = self.discovery)
    broadcast = threading.Thread(target = self.broadcast)
    discovery.daemon = True
    broadcast.daemon = True
        
    discovery.start()
    broadcast.start()

    
    app.run(host = '0.0.0.0', port = 54001, debug = True)
