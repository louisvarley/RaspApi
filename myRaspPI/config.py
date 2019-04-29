
title = ""
uiversion = 2
port = 5555
swagger = None
workingDir = None
version = 0
updater = None
discoveryMonitor = None
discoveryBroadcast = None
flask = None

#Get The Version as of NOW
def getVersion():
    with open(workingDir + '/VERSION') as f:
        return int(f.readline())

def getFullVersion():
    return "v1.0." + str(getVersion())

def hasVersionChanged():

    if(int(getVersion()) > int(version)):
        return True
    else:
        return False

def restart():
    logging.loggingService.logInfo("Restarting following update...")
    os.execv(sys.executable, ['python3'] + sys.argv)
    