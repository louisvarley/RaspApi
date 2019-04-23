import json
import flasgger

from flask import Flask, jsonify, redirect
from urllib.request import urlopen
from flasgger import Swagger
from flasgger.utils import swag_from

class swagRemote():
    """ Static Class for some Remote Swagging Toolsets """

    def swagFromURL(url,app,swagger):
        #Replace with URL
        with urlopen("https://petstore.swagger.io/v2/swagger.json") as url:
            data = json.loads(url.read().decode())

        for path in data['paths']:
            exec("""
@app.route('""" + str(path) + """')
@swag_from(""" + str(data['paths'][path]) + """)
def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
    return {'response':'response'}
        """)  
