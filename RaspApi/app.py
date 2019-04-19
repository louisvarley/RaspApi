"""
This script runs the RaspApi application using a development server.
"""

from os import environ
from RaspApi import app

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

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
