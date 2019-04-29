import os
import sys
import myRaspPI

from myRaspPI.utils import logging
from flask import Flask
app = Flask(__name__)

myRaspPI.workingDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
myRaspPI.title = "myRaspPI"
myRaspPI.uiversion = 2
myRaspPI.port = 5555
myRaspPI.swagger = None
myRaspPI.flask = None
myRaspPI.build = 0
myRaspPI.updater = None
myRaspPI.discoveryMonitor = None
myRaspPI.discoveryBroadcast = None

def getBuild():
    with open(workingDir + '/build_number') as f:
        return f.readline()

def buildChanged():

    if(myRaspPI.build == 0):
        myRaspPI.build = getBuild()

    if(int(getBuild()) > int(myRaspPI.build)):
        return True
    else:
        return False

def restart():
    logging.loggingService.logInfo("Restarting following update...")
    os.execv(sys.executable, ['python3'] + sys.argv)