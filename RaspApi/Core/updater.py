import pip
from subprocess import check_call as run 
from getopt import getopt, GetoptError 
import os 

class updateService(object):
    
    def checkForUpdate(workingDir):

        print("Fetching most recent code from source..." + workingDir)
        # Fetch most up to date version of code.
        cmd = ("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "fetch", "origin", "master", _out=ProcessFetch, _out_bufsize=0, _tty_in=True)               
        run(cmd)

        print("Fetch complete.")
        time.sleep(2)
        print("Checking status for " + workingDir + "...")

        cmd = ("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "status")
        run(cmd)

        if "Your branch is up-to-date" in statusCheck:
            print("Status check passes.")
            print("Code up to date.")
            return False
        else:
            print("Code update available.")
            return True

    def update(workingDir):
        resetCheck = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "reset", "--hard", "origin/master")
