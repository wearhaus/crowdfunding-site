import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'This is the main site'

@app.route('/<referral>')
def main_special(referral):
    return 'This is the page for people with the %s code' % referral
