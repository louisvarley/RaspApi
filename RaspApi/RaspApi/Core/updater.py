import pip
from subprocess import check_call as run 
from getopt import getopt, GetoptError 
import os 


class updateService(object):
    
    def update(): 
        dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

        cmd = 'git init "' + dir + '"'
        run(cmd)
        
        cmd = "git remote add origin https://github.com/louisvarley/RaspApi.git"
        run(cmd)
        cmd = "git branch --set-upstream-to=origin/master master"
        run(cmd)
        cmd = "git fetch"
        run(cmd)
        cmd = "git pull"
        run(cmd)