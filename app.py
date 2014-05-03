import os

from flask import Flask, redirect, render_template, request, url_for
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

@app.route('/thankyou', methods=['GET'])
def thank_you():
    print "Thank you page"
    email = str(request.args.get('email'))
    # Check if we already have that email stored, if so just return
    user = User.query.filter_by(email=email).first()
    if user:
        print user
        return render_template('thankyou.html', email=user.email, code=user.referral_code)

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
    return render_template('thankyou.html')


@app.route('/<referral>')
def main_special(referral):
    print referral
    if promo.get(referral):
        print "awesome"
        data = grab_campaign_data()
        return render_template('index.html', code=promo.get(referral)['code'], discount=promo.get(referral)['amount'], **data)
    return redirect('/')


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


def create_user(email, code):
    user = User(email, code)
    db.session.add(user)
    db.session.commit()


def add_referral_code(code):
    referral_code = ReferralCode(code)
    db.session.add(referral_code)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
