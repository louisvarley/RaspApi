import logging

class loggingService(object):
    """Static Logging Class"""
        
    def logDebug(str):
        logging.basicConfig(filename='RaspApi.log',level=logging.DEBUG)
        logging.debug(str)
        print(str)

    def logInfo(str):
        logging.basicConfig(filename='RaspApi.log',level=logging.INFO)
        logging.info(str)
        print(str)

    def logWarning(str):
        logging.basicConfig(filename='RaspApi.log',level=logging.WARNING)
        logging.warning(str)
        print(str)




