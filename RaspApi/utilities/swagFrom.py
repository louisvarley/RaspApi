from flask import Flask, jsonify, redirect
from urllib.request import urlopen
import json

class swagFrom(object):

    def __init__(self):
        print("")
    
    def call(self,path,swag):
        with urlopen("https://my-landscape-inst-api-uat.azurewebsites.net/swagger/docs/v1") as url:
            data = json.loads(url.read().decode())
        swagrtn = ""
        for path in data['paths']:
            swagrtn = swagrtn + self.loadRemoteSwagResource(str(path),str(data['paths'][path]))

        return swagrtn
            

    def loadRemoteSwagResource(self,path,swag):
                return("""
@app.route('""" + str(path) + """')
#@swag_from(""" + str(path) + """)
def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
    return {'response':'response'}
    """)
