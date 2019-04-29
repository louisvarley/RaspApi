from urllib.request import urlopen
from threading import Thread
from time import sleep
from myRaspPI.core import logging

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
        logging.loggingService.logInfo(" * Starting RaspiApi v1.0." + str(self.getLocalBuild()))
        
        while 1:
            if self.checkForUpdate():
                self.update()
            sleep(60)   

    def getLocalBuild(self):
        with open(myRaspPI.workingDir + '/build_number') as f:
            thisBuild = f.readline()
        return thisBuild

    def getRemoteBuild(self):
        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/myRaspPI/master/build_number"
        with urlopen(gitBuildUri) as url:
            remoteBuild = url.read().decode()
        return remoteBuild

    def checkForUpdate(self):
     
        localBuild = self.getLocalBuild()
        remoteBuild = self.getRemoteBuild()

        if(localBuild < remoteBuild):
            logging.loggingService.logInfo("A new update is available")
            return True
        else:
            return False

    def update(self):

        gitArchiveUri = "https://github.com/louisvarley/myRaspPI/archive/master.zip"
        remoteBuild = self.getRemoteBuild()
        
        logging.loggingService.logInfo("Downloading Update..." )

        #Download ZIP and extract
        with urlopen(gitArchiveUri) as r:
            with zipfile36.ZipFile(io.BytesIO(r.read()), "r") as z:
                logging.loggingService.logInfo("Installing Update..." )
                z.extractall(myRaspPI.workingDir)
     
        #Replace Local files
        rootSrcDir = myRaspPI.workingDir + "/myRaspPI-master"
        rootTargetDir = myRaspPI.workingDir

        for srcDir, dirs, files in os.walk(rootSrcDir):
            dstDir = srcDir.replace(rootSrcDir, rootTargetDir)
            if not os.path.exists(dstDir):
                os.mkdir(dstDir)
            for file_ in files:
                srcFile = os.path.join(srcDir, file_)
                dstFile = os.path.join(dstDir, file_)
                if os.path.exists(dstFile):
                    os.remove(dstFile)
                    shutil.move(srcFile, dstDir)

        #Remove temp
        if os.path.exists(rootSrcDir):
            print("Removing " + rootSrcDir)
            shutil.rmtree(rootSrcDir)
        
        logging.loggingService.logInfo("Version 1.0." + str(remoteBuild) + " successfully installed")

