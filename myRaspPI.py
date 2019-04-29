import urllib 
import ssl
import threading
import flasgger
import time
import os
import sys

import myRaspPI
from myRaspPI.services import discovery, updater
from myRaspPI.utils import logging, swagUtils

from time import sleep
from os import environ

from urllib.request import urlopen
from flask import Flask, redirect
from flasgger.utils import swag_from
from flasgger import Swagger

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

app.config['SWAGGER'] = {
  'title': myRaspPI.title,
  'uiversion': myRaspPI.uiversion
}

swagger = Swagger(app)
swagUtils.swagRemote.swagFromClient("https://petstore.swagger.io/v2/swagger.json","PetShop",app,swagger)

@app.route('/')
def root():
    return redirect("/apidocs/", code=302)

if __name__ == '__main__':

    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        myRaspPI.port = int(environ.get('SERVER_PORT', myRaspPI.port))
    except ValueError:
        myRaspPI.port = 5555

    #Start Update Service Thread
    updateService = updater.updateService()   
    updateService.setName('Updater Service')
    updateService.daemon = True
    updateService.start()
    myRaspPI.updateService = updateService

    #Start Flask Service Thread
    flask = threading.Thread(target=app.run,args=(HOST, myRaspPI.port))
    flask.setName('Flask Server')
    flask.daemon = True
    flask.start()
    myRaspPI.flask = flask

    #Start the Discovery Monitor Service
    discoveryMonitor = discovery.Monitor()
    discoveryMonitor.setName('Monitor Service')
    discoveryMonitor.daemon = True
    discoveryMonitor.start()
    myRaspPI.discoveryMonitor = discoveryMonitor

    #Start the Discovery Broadcast Service
    discoveryBroadcast = discovery.Broadcast()
    discoveryBroadcast.setName('Broadcast Service')
    discoveryBroadcast.daemon = True
    discoveryBroadcast.start()
    myRaspPI.discoveryBroadcast = discoveryBroadcast

    while True:
        time.sleep(1)

        if(myRaspPI.buildChanged() == True):                  
            myRaspPI.restart()