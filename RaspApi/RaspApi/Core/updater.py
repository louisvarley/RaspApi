import pip
from subprocess import check_call as run 
from getopt import getopt, GetoptError 
import os 


class updateService(object):
    
    def update(): 
        dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
        cmd = "git clone git@github.com:louisvarley/RaspApi.git " + dir
        run(cmd)