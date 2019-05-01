import myRaspPI
from myRaspPI import config, core 
from myRaspPI.core import discovery, updater, logging, swagUtils

import urllib, ssl, threading, flasgger, time, os, sys
from time import sleep
from os import environ
from urllib.request import urlopen
from flask import Flask, redirect
from flasgger.utils import swag_from
from flasgger import Swagger

def main():

    #App Config Defaults
    myRaspPI.config.workingDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    myRaspPI.config.title = "myRaspPI"
    myRaspPI.config.uiversion = 2
    myRaspPI.config.port = 5555
    myRaspPI.config.version = myRaspPI.config.getVersion()

    ssl._create_default_https_context = ssl._create_unverified_context
    app = Flask(__name__)

    app.config['SWAGGER'] = {
      'title': config.title,
      'uiversion': config.uiversion
    }

    swagger = Swagger(app)
    swagUtils.swagRemote.swagFromClient("https://petstore.swagger.io/v2/swagger.json","PetShop",app,swagger)

    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        myRaspPI.config.port = int(environ.get('SERVER_PORT', myRaspPI.config.port))
    except ValueError:
        myRaspPI.config.port = 5555

    @app.route('/')
    def root():
        return redirect("/apidocs/", code=302)

    #Start Update Service Thread
    updateService = updater.updateService()   
    updateService.setName('Updater Service')
    updateService.daemon = True
    updateService.start()
    myRaspPI.config.updateService = updateService

    #Start Flask Service Thread, Save to Config
    flask = threading.Thread(target=app.run,args=(HOST, myRaspPI.config.port))
    flask.setName('Flask Server')
    flask.daemon = True
    flask.start()
    myRaspPI.config.flask = flask

    #Start the Discovery Monitor Service, Save to Config
    discoveryMonitor = discovery.Monitor()
    discoveryMonitor.setName('Monitor Service')
    discoveryMonitor.daemon = True
    discoveryMonitor.start()
    myRaspPI.config.discoveryMonitor = discoveryMonitor

    #Start the Discovery Broadcast Service, Save to Config
    discoveryBroadcast = discovery.Broadcast()
    discoveryBroadcast.setName('Broadcast Service')
    discoveryBroadcast.daemon = True
    discoveryBroadcast.start()
    myRaspPI.config.discoveryBroadcast = discoveryBroadcast

    logging.loggingService.logInfo(" * Starting RaspiApi v1.0." + str( myRaspPI.config.getVersion()))

    while True:
        time.sleep(1)
        if(myRaspPI.config.hasVersionChanged() == True):                  
            myRaspPI.config.restart()

if __name__ == '__main__':
    main()


