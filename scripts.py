import json
import urllib2

from app import User
from sqlalchemy import func


def promo_code_counts():
    j = urllib2.urlopen('https://wearhaus.crowdhoster.com/api/campaigns/3/payments?api_key=d2e5116bb53855961394')
    payments = json.load(j)
    counts = {}
    for payment in payments:
        if payment.get('promo_code'):
            code = payment.get('promo_code').get('code')
            if code in counts:
                counts[code] += 1
            else:
                counts[code] = 1
    return counts

def email_refund_counts():
    promo_code_uses = promo_code_counts()
    email_counts = {}
    for code in promo_code_uses:
        user = User.query.filter(func.lower(User.referral_code) == func.lower(code)).first()
        if user:
            email_counts[user.email] = promo_code_uses[code]
    return email_counts


if __name__ == "__main__":
    for email, count in email_refund_counts().iteritems():
        print str(email) + ": " + str(count)
