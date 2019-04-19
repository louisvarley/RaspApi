"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from RaspApi import app

@app.route('/')
def root():
 return redirect("/apidocs/", code=302)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
