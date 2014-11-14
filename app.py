import json
import os
import time
import urllib2

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func

from promo import promo
from util import days_until, grab_campaign_data, parse_date, payments_by_promo_code


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def main():
    print "Loaded front page"
    data = grab_campaign_data()
    return render_template('index.html', **data)
    
@app.route('/zh')
def main_zh():
    print "Loaded front page in Chinese"
    data = grab_campaign_data()
    data['raised'] = int(data['raised']*6.25)
    return render_template('index_zh.html', **data)

@app.route('/faq')
def faq():
    data = grab_campaign_data()
    return render_template('faq.html', **data)

@app.route('/video')
def video():
    return redirect('https://www.youtube.com/watch?v=1JzJsSjQaiI')

@app.route('/kickstarter')
def kickstarter():
    return redirect('https://www.kickstarter.com/projects/1445900023/wearhaus-arc-wireless-headphones-reinvented')

@app.route('/zh/faq')
def faq_zh():
    data = grab_campaign_data()
    data['raised'] = int(data['raised']*6.25)
    return render_template('faq_zh.html', **data)

@app.route('/promocode')
def promocode():
    code = str(request.args.get('code'))
    if code == "None":
        return render_template('promocode.html')
    else:
        payments = payments_by_promo_code(code.upper())
        payments.sort(key=lambda payment: time.strptime(payment.get('created_at'), '%Y-%m-%dT%H:%M:%S+00:00'))
        print payments
        dollar_total = sum([payment.get('amount') for payment in payments])/100
        single_unit_total = len(filter(lambda p: p.get('reward_id')==10, payments))
        couples_pack_total = len(filter(lambda p: p.get('reward_id')==11, payments))
        unit_total = single_unit_total + (2 * couples_pack_total)
        return render_template('promocode.html', code=code, payments=payments, dollar_total=dollar_total, unit_total=unit_total)


@app.route('/referral', methods=['GET'])
def referral():
    email = str(request.args.get('email'))
    if email == "None":
        return render_template('referral.html')

    user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
    if user:
        payments = payments_by_promo_code(user.referral_code)
        return render_template('referral.html', email=user.email, code=user.referral_code, code_users=len(payments))
    else:
        return render_template('referral.html', unrecognized_email=True)


@app.route('/thankyou', methods=['GET'])
def thank_you():
    print "Thank you page"
    email = str(request.args.get('email'))
    confirmation_id = str(request.args.get('confirmation_id'))
    transaction_amount = 0;
    print email
    if email == "None":
        print "No email"
        return render_template('thankyou.html', confirmation_id=confirmation_id, transaction_amount=transaction_amount)
    # Check if we already have that email stored, if so just return
    user = User.query.filter(func.lower(User.email) == func.lower(email)).first()

    j = urllib2.urlopen('https://wearhaus.crowdhoster.com/api/campaigns/3/payments?api_key=d2e5116bb53855961394')
    payments = json.load(j)

    for payment in payments:
        if payment.get('ct_payment_id') == confirmation_id:
            amount = payment.get('amount')
            if amount:
                amount = str(amount)
                transaction_amount = amount[:3] + '.' + amount[3:]

    if user and user.referral_code:
        return render_template('thankyou.html', email=user.email, code=user.referral_code, confirmation_id=confirmation_id, transaction_amount=transaction_amount)

    for payment in payments:
        if payment['email'] == email:
            print payment
            # Grab referral code from that payment index
            payment_id = payment.get(u'id')
            print payment_id
            referral_code = ReferralCode.query.all()[payment_id].referral_code
            print referral_code
            user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
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
            return render_template('thankyou.html', email=user.email, code=user.referral_code, confirmation_id=confirmation_id, transaction_amount=transaction_amount)

    user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
    if email and not user:
        return render_template('thankyou.html', unrecognized_email=True, email=email, confirmation_id=confirmation_id, transaction_amount=transaction_amount)

    return render_template('thankyou.html', error=True, confirmation_id=confirmation_id, transaction_amount=transaction_amount)


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
