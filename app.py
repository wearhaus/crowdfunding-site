import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/<referral>')
def main_special(referral):
    return 'This is the page for people with the %s code' % referral
