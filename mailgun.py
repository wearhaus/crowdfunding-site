import requests

from app import User


def send_emails():
    users = User.query.all()
    for user in users:
        print user.email, type(user.email)
        print user.referral_code, type(user.referral_code)
        send_halfway_message(user.email, user.referral_code)

def send_halfway_message(email, code):
    return requests.post(
        "https://api.mailgun.net/v2/wearhaus.com/messages",
        auth=("api", "key-7zkje172t17djruxxkgq5kfo4v4f55x1"),
        files=[("inline", open("static/email/halfway.png"))],
        data={"from": "Wearhaus Inc. <team@wearhaus.com>",
              "to": [email],
              "subject": "We're halfway there!",
              "text": "It's been a crazy week! We've already reached half of our $75,000 goal! Thank you SO much for all of your support! We're incredibly excited to get the Wearhaus Arc in your hands.\nWe still have 27 more days to reach our goal, but we need your help. Please spread the word about Wearhaus and our campaign to as many friends as you can!\nWearhaus Arc is more fun with friends. We want to help you get them on board as well! We've given you a unique referral discount code and link for you to pass around to your friends and family. Every time someone uses your discount code, they get $15 off their purchase, and you'll get $15 refunded as well! We'll count up all of your referrals at the end of the campaign and refund you the total amount within two weeks after.\nYour unique referral link is: http://wearhaus.com/{0}\nPlease share this on your social media channels!".format(code),
              "html": """
<h1 style="font-family:verdana; text-align:center; color:#00bccc;">WE'RE HALFWAY THERE!</h1>
<img src="cid:halfway.png" height="auto" width="100%">
<p>It's been a crazy week! We've already reached half of our $75,000 goal! Thank you SO much for all of your support! We're incredibly excited to get the Wearhaus Arc in your hands.</p>
<p>We still have 27 days to reach our goal, but we need your help. We need EVERYONE to spread the word about Wearhaus to as many friends as possible!</p>
<h2 style="font-family:verdana; text-align:center; ">Want your headphones for free?</h2>
<p>Wearhaus Arc is more fun with friends, so we want to help you get them on board as well! We've given you a unique referral discount code and link for you to pass around to your friends and family    . Every time someone uses your discount code, they get $15 off their purchase, and you'll get $15 refunded as well! We'll count up all of your referrals at the end of the campaign and refund you the     total amount within two weeks.</p>
<h3 style="font-family:verdana; text-align:center;">Your referral link is:</h3>
<h3 style="font-family:verdana; text-align:center; color:#00bccc;">http://wearhaus.com/{0}</h3>
<div style="width:250px; margin-left:auto; margin-right:auto;">
    <a href="https://www.facebook.com/sharer/sharer.php?u=http://campaign.wearhaus.com/{0}"><p style="float:left;">Share on Facebook</p></a>
        <a href="https://twitter.com/home?status=Check%20out%20Arc%20social%20music%20listening%20headphones%20by%20@WearhausInc!%20Use%20this%20link%20for%20$15%20off!%20http://wearhaus.com/{0}%20%23WearhausArc"><p style="float:right;">Share on Twitter</p></a>
        </div>""".format(code)})
