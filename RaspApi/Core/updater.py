import urllib

class updateService(object):
    
    def checkForUpdate(workingDir):
        with open('build_number') as f:
            thisBuild = f.readline()

        gitBuildUri = " https://raw.githubusercontent.com/louisvarley/RaspApi/master/build_number"
        f = urllib.urlopen(gitBuildUri)
        currentBuild = f.read()
           
        if(thisBuild != currentBuild):
            return True
        else:
            return False
                

    def update(workingDir):
        resetCheck = git("--git-dir=" + workingDir + ".git/", "--work-tree=" + workingDir, "reset", "--hard", "origin/master")
