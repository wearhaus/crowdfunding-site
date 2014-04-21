import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/<referral>')
def main_special(referral):
    return 'This is the page for people with the %s code' % referral
