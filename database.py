from app import db, ReferralCode, User


def create_user(email, code):
    user = User(email, code)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print "Aborted create_user"

def add_referral_code(code):
    referral_code = ReferralCode(code)
    try:
        db.session.add(referral_code)
        db.session.commit()
    except:
        db.session.rollback()
        print "Aborted add_referral_code"

def load_referral_codes(path):
    with open(path, 'r') as f:
        code = f.readline()[:-1]
        while code:
            print code
            add_referral_code(code)
            code = f.readline()[:-1]
    print ReferralCode.query.all()
