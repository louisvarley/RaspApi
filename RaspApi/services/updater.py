from urllib.request import urlopen
from threading import Thread
from time import sleep
from RaspApi.services import logging

import zipfile36
import glob, os, shutil
import io



class updateService(Thread):
    """Updates the current version automaticly, run as thread"""

    def __init__(self, workingDir):
        Thread.__init__(self)
        logging.loggingService.logInfo(" * Starting Auto Updater...")
        self.workingDir = workingDir
    
    def run(self):
        logging.loggingService.logInfo(" * Running RaspiApi v1.0." + str(self.getLocalBuild()))
        
        while 1:
            if self.checkForUpdate():
                self.update()
            sleep(60)   

    def getLocalBuild(self):
        with open(self.workingDir + '/build_number') as f:
            thisBuild = f.readline()
        return thisBuild

    def getRemoteBuild(self):
        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/RaspApi/master/build_number"
        with urlopen(gitBuildUri) as url:
            remoteBuild = url.read().decode()
        return remoteBuild

    def checkForUpdate(self):
     
        localBuild = self.getLocalBuild()
        remoteBuild = self.getRemoteBuild()
           
        if(localBuild < remoteBuild):
            logging.loggingService.logInfo("Version 1.0." + str(remoteBuild) + " is available")
            return True
        else:
            return False
                

    def update(self):

        gitArchiveUri = "https://github.com/louisvarley/RaspApi/archive/master.zip"
        remoteBuild = self.getRemoteBuild()
        
        logging.loggingService.logInfo("Downloading Update..." )

        #Download ZIP and extract
        with urlopen(gitArchiveUri) as r:
            with zipfile36.ZipFile(io.BytesIO(r.read()), "r") as z:
                logging.loggingService.logInfo("Installing Update..." )
                z.extractall(self.workingDir)
     
        #Replace Local files
        rootSrcDir = self.workingDir + "/RaspApi-master"
        rootTargetDir = self.workingDir

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
            shutil.rmtree(rootSrcDir)
        
        logging.loggingService.logInfo("Version 1.0." + str(remoteBuild) + " successfully installed")

