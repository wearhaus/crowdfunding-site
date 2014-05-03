import os

from flask import Flask, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

#from database import db_session
#from models import User, ReferralCode
from promo import promo
from util import days_until, grab_campaign_data, parse_date


app = Flask(__name__)


@app.route('/')
def main():
    print "Loaded front page"
    data = grab_campaign_data()
    return render_template('index.html', **data)

@app.route('/thankyou', methods=['GET'])
def thank_you():
    email = str(request.args.get('email'))
    return render_template('thankyou.html')
"""
    # Check if we already have that email stored, if so just return
    user = User.query.filter_by(email=email).first()
    if user:
        return render_template('index.html', code=user.referral_code)

    j = urllib2.urlopen('https://wearhaus.crowdhoster.com/api/campaigns/3/payments?api_key=d2e5116bb53855961394')
    payments = json.load(j)
    for payment in payments:
        if payment['email'] == email:
            # Grab referral code from that payment index
            payment_id = payment['id']
            #referral_code = ReferralCode.query.filter_by(id=payment_id).first()
            referral_code = "asdfasdf" #Placeholder

            user = User(email, referral_code)
            db_session.add(user)
            db_session.commit()
"""

@app.route('/<referral>')
def main_special(referral):
    if promo.get(referral):
        data = grab_campaign_data()
        return render_template('index.html', code=promo.get(referral)['code'], discount=promo.get(referral)['amount'], **data)
    return redirect('/')

#@app.teardown_appcontext
#def shutdown_session(exception=None):
    #b_session.remove()

if __name__ == "__main__":
    app.run(debug=True)
