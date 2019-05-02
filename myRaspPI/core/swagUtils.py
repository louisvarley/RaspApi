import json
import flasgger

from flask import Flask, jsonify, redirect
from urllib.request import urlopen
from flasgger import Swagger
from flasgger.utils import swag_from
import myRaspPI
from myRaspPI import config
import platform

class swagRemote():
    """ Static Class for some Remote Swagging Toolsets """

    def defaultRoutes(app,swagger):
        name = str(platform.uname()[1])
        route = '/' + name + "/getClientInfo"

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
        with urlopen(jsonUrl) as url:
            data = json.loads(url.read().decode())
          

        for path in data['paths']:
            route = '/' + name + str(path)
            exec("""
@app.route('""" + str(route) + """')
@swag_from(""" + str(data['paths'][path]) + """)
def """ + str(path).replace("/","").replace("{","").replace("}","").replace(")","").replace("(","") + """():
    \"\"\" Example endpoint return a list of colors by palette 
    This is using docstring for specifications
    ---
    tags:
      - """ + name + """
    \"\"\"
    return "No"
        """)  
