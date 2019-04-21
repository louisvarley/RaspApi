from flask import Flask, jsonify, redirect
import json
import urllib

class swagFrom(object):
    
    def __init__(self,path,swag):
        url = urllib.urlopen("https://my-landscape-inst-api-uat.azurewebsites.net/swagger/docs/v1")
        data = json.loads(url.read().decode())

        for path in data['paths']:
            loadRemoteSwagResource(self,str(path),str(data['paths'][path]))

    def loadRemoteSwagResource(self,path,swag):
            exec("""
    @app.route('""" + str(path) + """')
    @swag_from(""" + str(data['paths'][path]) + """)
    def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
        return {'response':'response'}
            """)  
