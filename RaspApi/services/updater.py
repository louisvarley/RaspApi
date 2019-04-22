from urllib.request import urlopen
import zipfile36
import glob, os, shutil
import io

class updateService(object):
    
    def getLocalBuild(self):
        with open('build_number') as f:
            thisBuild = f.readline()
        return thisBuild

    def getRemoteBuild(self):
        gitBuildUri = "https://raw.githubusercontent.com/louisvarley/RaspApi/master/build_number"
        with urlopen(gitBuildUri) as url:
            remoteBuild = url.read().decode()
        return remoteBuild

    def checkForUpdate(self, workingDir):
     
        localBuild = self.getLocalBuild()
        remoteBuild = self.getRemoteBuild()
           
        if(localBuild < remoteBuild):
            return True
        else:
            return False
                

    def update(self, workingDir):

        gitArchiveUri = "https://github.com/louisvarley/RaspApi/archive/master.zip"
        print("Downloading Updates...")

        #Download ZIP and extract
        with urlopen(gitArchiveUri) as r:
            with zipfile36.ZipFile(io.BytesIO(r.read()), "r") as z:
                print("Installing Updates...")
                for file in z.namelist():
                    if file.startswith('RaspApi-master/'):
                        z.extract(file, workingDir)

        #Replace Local files
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

        #Remove temp
        if os.path.exists(rootSrcDir):
            shutil.rmtree(rootSrcDir)


