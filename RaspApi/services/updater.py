from urllib.request import urlopen
import zipfile36
import glob, os, shutil
import io

class updateService(object):
    
    def checkForUpdate(workingDir):
        with open('build_number') as f:
            thisBuild = f.readline()

        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/RaspApi/master/build_number"
        with urlopen(gitBuildUri) as url:
            remoteBuild = url.read().decode()

        print("This Build " + str(thisBuild))
        print("Available Build " + str(remoteBuild))
           
        if(thisBuild < remoteBuild):
            return True
        else:
            return False
                

    def update(workingDir):

        gitArchiveUri = "https://github.com/louisvarley/RaspApi/archive/master.zip"

        print("Downloading Updates...")

        #Download ZIP
        with urlopen(gitArchiveUri) as r:
            with zipfile36.ZipFile(io.BytesIO(r.read()), "r") as z:
                print("Installing Updates...")
                z.extract('RaspApi-master/', workingDir)