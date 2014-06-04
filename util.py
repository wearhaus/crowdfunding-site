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

def hours_until_end():
    seconds = 1402210799 - time.time() # Epoch time of Jun 7 11:59:59
    return max(0, int(seconds/3600))

def grab_campaign_data():
    try:
        j = urllib2.urlopen('https://checkout.wearhaus.com/api/campaigns/3?api_key=d2e5116bb53855961394')
        campaign = json.load(j)
        data = {
            'goal' : int(campaign.get('goal_dollars')),
            'raised' : int(campaign.get('stats_raised_amount', '75000')),
            'backers' : int(campaign.get('stats_number_of_contributions')),
            'days_remaining' : days_until(*parse_date(campaign.get('expiration_date'))),
            'hours_remaining' : hours_until_end(),
        }
    except:
        data = {
            'goal': 75000,
            'raised': 999999,
            'backers': 9999,
            'days_remaining': 30,
            'hours_remaining': 0,
        }

    data['percent'] = float(data.get('raised')) / data.get('goal') * 100
    data['progress'] = min(data.get('percent'), 100)
    return data
