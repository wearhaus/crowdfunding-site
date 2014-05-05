from app import db, ReferralCode, User


def create_user(email, code):
    user = User(email, code)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print "Aborted create_user"

def clear_users():
    for user in User.query.all():
        try:
            print "Deleting " + user.email
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            print "Aborted delete user"
    print User.query.all()

def clear_referral_codes():
    all_codes = ReferralCode.query.all()
    for code in all_codes:
        try:
            print "Deleting " + code.referral_code
            db.session.delete(code)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            print "Aborted delete code"
    print ReferralCode.query.all()

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
        print f
        code = f.readline()[:-1]
        while code:
            print code
            add_referral_code(code)
            code = f.readline()[:-1]
    print ReferralCode.query.all()
