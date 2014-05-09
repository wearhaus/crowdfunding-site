import json
import os
import urllib2

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from promo import promo
from util import days_until, grab_campaign_data, parse_date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def main():
    print "Loaded front page"
    data = grab_campaign_data()
    return render_template('index.html', **data)

@app.route('/faq')
def faq():
    data = grab_campaign_data()
    return render_template('faq.html', **data)

@app.route('/thankyou', methods=['GET'])
def thank_you():
    print "Thank you page"
    email = str(request.args.get('email'))
    confirmation_id = str(request.args.get('confirmation_id'))
    print email
    if email == "None":
        print "No email"
        return render_template('thankyou.html', confirmation_id=confirmation_id)
    # Check if we already have that email stored, if so just return
    user = User.query.filter_by(email=email).first()

    if user and user.referral_code:
        return render_template('thankyou.html', email=user.email, code=user.referral_code, confirmation_id=confirmation_id)

    j = urllib2.urlopen('https://wearhaus.crowdhoster.com/api/campaigns/3/payments?api_key=d2e5116bb53855961394')
    payments = json.load(j)
    for payment in payments:
        if payment['email'] == email:
            print payment
            # Grab referral code from that payment index
            payment_id = payment.get(u'id')
            print payment_id
            referral_code = ReferralCode.query.all()[payment_id].referral_code
            print referral_code
            user = User.query.filter_by(email=email).first()
            print user

            if user:
                user.referral_code = referral_code
            else:
                user = User(email, referral_code)

            print user
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                print e
                print "User commit failed. Rolling back"
                db.session.rollback()
            print User.query.all()
            return render_template('thankyou.html', email=user.email, code=user.referral_code, confirmation_id=confirmation_id)

    user = User.query.filter_by(email=email).first()
    if email and not user:
        return render_template('thankyou.html', unrecognized_email=True, email=email, confirmation_id=confirmation_id)

    return render_template('thankyou.html', error=True, confirmation_id=confirmation_id)


@app.route('/<referral>')
def main_special(referral):
    print referral
    referral = referral.lower()
    if promo.get(referral):
        data = grab_campaign_data()
        return render_template('index.html', code=promo.get(referral)['code'], discount=promo.get(referral)['amount'], **data)
    else:
        referral = referral.upper()
        if ReferralCode.query.filter(ReferralCode.referral_code == referral).first():
            data = grab_campaign_data()
            referral.upper()
            return render_template('index.html', code=referral, discount=15, **data)
    return redirect('/')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')


class User(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    referral_code = Column(String(20), unique=True)

    def __init__(self, email, referral_code):
        self.email = email
        self.referral_code = referral_code

    def __repr__(self):
        return '<User %r>' % self.email


class ReferralCode(db.Model):
    id = Column(Integer, primary_key=True)
    referral_code = Column(String(20), unique=True)

    def __init__(self, referral_code):
        self.referral_code = referral_code

    def __repr__(self):
        return '<Code %r>' % self.referral_code


if __name__ == "__main__":
    app.run(debug=True)
