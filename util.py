import json
import time
import urllib2
from datetime import date


def parse_date(_datetime):
    _date, _time = _datetime.split('T')
    year, month, day = _date.split('-')
    #_hour, _minute, _second = _time.split('+')[0].split(':')
    return (int(year), int(month), int(day))

def days_until(year, month, day):
    today = date.today()
    target_date = date(year, month, day)
    difference = abs(target_date - today)
    return difference.days

def grab_campaign_data():
    j = urllib2.urlopen('https://checkout.wearhaus.com/api/campaigns/3?api_key=d2e5116bb53855961394')
    campaign = json.load(j)

    data = {
        'goal' : int(campaign.get('goal_dollars')),
        'raised' : int(campaign.get('stats_raised_amount', '75000')),
        'backers' : campaign.get('stats_number_of_contributions'),
        'days_remaining' : days_until(*parse_date(campaign.get('expiration_date'))),
    }
    data['percent'] = float(data.get('raised')) / data.get('goal') * 100
    data['progress'] = min(data.get('percent'), 100)
    return data
