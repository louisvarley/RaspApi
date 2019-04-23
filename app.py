import urllib 
import ssl
import threading
import flasgger
import time
import os
import sys

import RaspApi
from RaspApi.services import discovery, updater
from RaspApi.utils import logging, swagUtils

from time import sleep
from os import environ
from urllib.request import urlopen
from flask import Flask, redirect

from flasgger.utils import swag_from
from flasgger import Swagger

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

app.config['SWAGGER'] = {
  'title': RaspApi.title,
  'uiversion': RaspApi.uiversion
}

swagger = Swagger(app)
swagUtils.swagRemote.swagFromURL("",app,swagger)

@app.route('/')
def root():
    return redirect("/apidocs/", code=302)

if __name__ == '__main__':

    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        RaspApi.port = int(environ.get('SERVER_PORT', RaspApi.port))
    except ValueError:
        RaspApi.port = 5555

    #Start Update Service Thread
    updateService = updater.updateService()   
    updateService.setName('Updater Service')
    updateService.daemon = True
    updateService.start()
    RaspApi.updateService = updateService

    #Start Flask Service Thread
    flask = threading.Thread(target=app.run,args=(HOST, RaspApi.port))
    flask.setName('Flask Server')
    flask.daemon = True
    flask.start()
    RaspApi.flask = flask

    #Start the Discovery Monitor Service
    discoveryMonitor = discovery.Monitor()
    discoveryMonitor.setName('Monitor Service')
    discoveryMonitor.daemon = True
    discoveryMonitor.start()
    RaspApi.discoveryMonitor = discoveryMonitor

    #Start the Discovery Broadcast Service
    discoveryBroadcast = discovery.Broadcast()
    discoveryBroadcast.setName('Broadcast Service')
    discoveryBroadcast.daemon = True
    discoveryBroadcast.start()
    RaspApi.discoveryBroadcast = discoveryBroadcast

    while True:
        time.sleep(1)

        if(RaspApi.buildChanged() == True):                  
            RaspApi.restart()