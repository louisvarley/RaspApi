import urllib
import json 
import ssl
import scapy.all as scapy
import argparse
import threading
import flasgger
import time
import os
import sys

from os import environ
from RaspApi import app
from RaspApi import views
from RaspApi.services import discovery, updater

from flask import Flask, jsonify, redirect
from flasgger import Swagger
from flasgger.utils import swag_from
from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)

app.config['SWAGGER'] = {
  'title': 'RaspApi',
  'uiversion': 2
}

swagger = Swagger(app)

@app.route('/')
def root():
    return redirect("/apidocs/", code=302)


if __name__ == '__main__':

    updateService = updater.updateService()    
    localDir = os.path.dirname(os.path.realpath(__file__))

    localBuild = updateService.getLocalBuild();

    print("v1.0." + str(updateService.getLocalBuild()))

    if updateService.checkForUpdate(localDir):
        print("Update Available [" + str(updateService.getRemoteBuild()) + "]. Installing...")
        updateService.update(localDir)
    else:
        print("No Updates")

    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    flask = threading.Thread(target=app.run,args=(HOST, PORT))
    flask.daemon = True
    flask.start()

    monitorService = discovery.Monitor(2)
    monitorService.setName('Monitor')
    monitorService.daemon = True
    monitorService.start()

    broadcastService = discovery.Broadcast(3)
    broadcastService.setName('Broadcast')
    broadcastService.daemon = True
    broadcastService.start()

    while True:
        time.sleep(1) #Main Loop Thread

        #Restart Main Thread if build has changed (updated)
        if(updateService.getLocalBuild() > localBuild):
            print("Restarting following update...")
            os.execv(sys.executable, ['python'] + sys.argv)