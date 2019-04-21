from urllib.request import urlopen
import zipfile36
import glob, os, shutil
import io

class updateService(object):
    
    def getBuild():
        with open('build_number') as f:
            thisBuild = f.readline()
        return thisBuild

    def checkForUpdate(workingDir):
     
        thisBuild = getBuild()
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

                for file in z.namelist():
                    if file.startswith('RaspApi-master/'):
                        z.extract(file, workingDir)

        rootSrcDir = workingDir + "/RaspApi-master"
        rootTargetDir = workingDir

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
        if os.path.exists(rootSrcDir):
            os.remove(rootSrcDir)


