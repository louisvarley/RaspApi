from urllib.request import urlopen
from threading import Thread
from time import sleep
from core import logging

import zipfile36
import glob, os, shutil
import io
import myRaspPI

class updateService(Thread):
    """Updates the current version automaticly, run as thread"""

    def __init__(self):
        Thread.__init__(self)
        logging.loggingService.logInfo(" * Starting Auto Updater...")
    
    def run(self):
        logging.loggingService.logInfo(" * Starting RaspiApi v1.0." + str( myRaspPI.config.getVersion()))
        
        while 1:
            if self.checkForUpdate():
                self.update()
            sleep(60)   

    def getRemoteVersion(self):
        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/myRaspPI/master/VERSION"
        with urlopen(gitBuildUri) as url:
            remoteVersion = int(url.read().decode())
        return remoteVersion

    def getFullRemoteVersion(self):
        return "v1.0." + str(self.getRemoteVersion())

    def checkForUpdate(self):
     
        localVersion = myRaspPI.config.getVersion()
        remoteVersion = self.getRemoteVersion()

        if(localVersion < remoteVersion):
            logging.loggingService.logInfo("A new update is available")
            return True
        else:
            return False

    def update(self):

        startVersion = myRaspPI.config.getVersion()

        gitArchiveUri = "https://github.com/louisvarley/myRaspPI/archive/master.zip"
        remoteVersion = self.getRemoteVersion()

        logging.loggingService.logInfo("Downloading Update..." )

        os.system("pip3 install --upgrade --no-deps git+git://github.com/louisvarley/myRaspPI@master")

        if(startVersion == remoteVersion):
            logging.loggingService.logInfo(myRaspPI.config.getFullVersion() + " installed successfully")
        else:
            logging.loggingService.logInfo(self.getFullRemoteVersion() + " installation failed")

