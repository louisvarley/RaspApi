import json
import flasgger
import myRaspPI
import platform
import sys

from flask import Flask, jsonify, redirect
from urllib.request import urlopen
from flasgger import Swagger
from flasgger.utils import swag_from
from myRaspPI.core import logging
from myRaspPI import config

def defaultRoutes(app,swagger):
    name = str(platform.uname()[1])
    route = '/' + name.upper() + '/getClientInfo'

    specs_dict = {
        "parameters": [
        {
            "name": "palette",
            "in": "path",
            "type": "string",
            "enum": [
            "all",
            "rgb",
            "cmyk"
            ],
            "required": "true",
            "default": "all"
        }
        ],
        "definitions": {
        "Palette": {
            "type": "object",
            "properties": {
            "palette_name": {
                "type": "array",
                "items": {
                "$ref": "#/definitions/Color"
                }
            }
            }
        },
        "Color": {
            "type": "string"
        }
        },
        "responses": {
        "200": {
            "description": "A list of colors (may be filtered by palette)",
            "schema": {
            "$ref": "#/definitions/Palette"
            },
            "examples": {
            "rgb": [
                "red",
                "green",
                "blue"
            ]
            }
        }
        }
    }

    exec("""
@app.route('""" + str(route) + """')
@swag_from(specs_dict)
def routeClientInfo():
    \"\"\" Example endpoint return a list of colors by palette 
    This is using docstring for specifications
    ---
    tags:
      - """ + name + """
    \"\"\"
    return "No"
        """)  

def swagFromClient(jsonUrl,name,app,swagger):

    #Replace with URL
    try:
        with urlopen(jsonUrl) as url:
            data = json.loads(url.read().decode())
    except: 
        logging.loggingService.logInfo("Unable to swag from " + jsonUrl)
          

    for path in data['paths']:
        try:
            
            route = '/' + name + "/" + str(path).split("/")[-1]
            if(name in data['paths'][path]['get']['tags']):

                print("Loading... @" + name + ' ' + route)
                exec("""
@app.route('""" + str(route) + """')
@swag_from(""" + str(data['paths'][path]) + """)
def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
    \"\"\" Example endpoint return a list of colors by palette 
    This is using docstring for specifications
    ---
    tags:
      - """ + name.upper() + """
    \"\"\"
    return "No"
        """)  
        except:
            logging.loggingService.logInfo("Error while creating endpoint for " + route)
            logging.loggingService.logInfo(sys.exc_info()[0])
            
