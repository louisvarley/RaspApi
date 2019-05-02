import myRaspPI
import signal
from myRaspPI import config, core 
from myRaspPI.core import discovery, updater, logging, swagUtils

import urllib, ssl, threading, flasgger, time, os, sys, subprocess, platform, os

from time import sleep
from os import environ
from urllib.request import urlopen
from flask import Flask, redirect
from flasgger.utils import swag_from
from flasgger import Swagger
from multiprocessing import Process, Queue

def main():

    #App Config Defaults
    myRaspPI.config.workingDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    myRaspPI.config.title = "myRaspPI"
    myRaspPI.config.uiversion = 2
    myRaspPI.config.port = 5555
    myRaspPI.config.version = myRaspPI.config.getVersion()
    myRaspPI.config.hostName = str(platform.uname()[1])

    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        myRaspPI.config.port = int(environ.get('SERVER_PORT', myRaspPI.config.port))
    except ValueError:
        myRaspPI.config.port = 5555

    #Start Update Service Thread
    updateService = updater.updateService()   
    updateService.setName('Updater Service')
    updateService.daemon = True
    updateService.start()
    myRaspPI.config.updateService = updateService

    #Start Flask Service Thread, Save to Config


    #Start the Discovery Monitor Service, Save to Config
    discoveryMonitor = discovery.DiscoveryMonitor()
    discoveryMonitor.setName('Monitor Service')
    discoveryMonitor.daemon = True
    discoveryMonitor.start()
    myRaspPI.config.discoveryMonitor = discoveryMonitor

    #Start the Discovery Broadcast Service, Save to Config
    discoveryBroadcast = discovery.DiscoveryBroadcast()
    discoveryBroadcast.setName('Broadcast Service')
    discoveryBroadcast.daemon = True
    discoveryBroadcast.start()
    myRaspPI.config.discoveryBroadcast = discoveryBroadcast

    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'uiversion': 2,
        'title': myRaspPI.config.title,
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
        "specs": [
            {
                "version":myRaspPI.config.getFullVersion(),
                "title": myRaspPI.config.hostName,
                "endpoint": 'v1_spec',
                "description": "myRaspPI Client",
                "route": '/spec.json',
            }
        ]
    }


    @app.route('/')
    def root():
        return redirect("/apidocs/", code=302)

    swagger = Swagger(app)

    myRaspPI.config.host = environ.get('SERVER_HOST', '0.0.0.0')

    logging.loggingService.logInfo(" * Starting RaspiApi v1.0." + str( myRaspPI.config.getVersion()))
    swagUtils.swagRemote.swagFromClient("https://petstore.swagger.io/v2/swagger.json","test",app,swagger)

    flask = threading.Thread(target=app.run,args=(myRaspPI.config.host, myRaspPI.config.port))
    flask.setName('Flask Server')
    flask.daemon = True
    flask.start()
    myRaspPI.config.flask = flask


    while True:
        
        if(myRaspPI.config.hasVersionChanged() == True):                  
            myRaspPI.config.restart()

        for ipAddress, client in myRaspPI.config.discoveryMonitor.clients.clientList.items():
            if(myRaspPI.config.discoveryMonitor.clients.isClientOnline(client.ipAddress)):
                if(client.loaded == False):
                    client.loaded = True

                    os.kill(flask.ident,signal.SIGKILL)

                    try:
                        swagUtils.swagRemote.swagFromClient("https://petstore.swagger.io/v2/swagger.json",client.hostName,app,swagger)
                        time.sleep(0)
                    except:
                        time.sleep(0)

                    logging.loggingService.logInfo(" * Starting RaspiApi v1.0." + str( myRaspPI.config.getVersion()))
                    flask = threading.Thread(target=app.run,args=(myRaspPI.config.host, myRaspPI.config.port))
                    flask.setName('Flask Server')
                    flask.daemon = True
                    flask.start()
                    myRaspPI.config.flask = flask

        time.sleep(1) 


if __name__ == '__main__':
    main()

