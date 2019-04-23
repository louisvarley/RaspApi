import os
import sys
import RaspApi

from RaspApi.utils import logging
from flask import Flask
app = Flask(__name__)

RaspApi.workingDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
RaspApi.title = "RaspAPI"
RaspApi.uiversion = 2
RaspApi.port = 5555
RaspApi.swagger = None
RaspApi.flask = None
RaspApi.build = 0
RaspApi.updater = None
RaspApi.discoveryMonitor = None
RaspApi.discoveryBroadcast = None

def getBuild():
    with open(workingDir + '/build_number') as f:
        return f.readline()

def buildChanged():

    if(RaspApi.build == 0):
        RaspApi.build = getBuild()

    if(int(getBuild()) > int(RaspApi.build)):
        return True
    else:
        return False

def restart():
    logging.loggingService.logInfo("Restarting following update...")
    os.execv(sys.executable, ['python3'] + sys.argv)