import urllib
import json 
import ssl
import scapy.all as scapy
import argparse
import threading
import flasgger
import time

from os import environ
from RaspApi import app
from RaspApi.Core import discovery, updater
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

if __name__ == '__main__':

    i = updater.updateService
    i.update()

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
        time.sleep(10) #Main Loop Thread