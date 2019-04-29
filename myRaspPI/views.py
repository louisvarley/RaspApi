"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from myRaspPI import app

@app.route('/')
def root():
 return redirect("/apidocs/", code=302)
