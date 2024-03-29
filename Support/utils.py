#!/usr/bin/env python3

import requests
import datetime

token = '5490134622:AAHU3d8mZWRon9pSqK3t7dOt9SgbFYVW7PI'
method = 'sendMessage'
chat_id = '-1001576496655'

def log(msg, telegram=False):
    print(str(datetime.datetime.now(tz=EST5EDT()).date()) + " " + str(datetime.datetime.now(tz=EST5EDT()).time()) + ": " + msg)
    if (telegram):
        msg = str(datetime.datetime.now(tz=EST5EDT()).date()) + " " + str(datetime.datetime.now(tz=EST5EDT()).time()) + ": " + msg
        requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': chat_id, 'text': msg}
        )

def isTradeTime(begin_time, end_time):
    # If check time is not given, default to current UTC time
    check_time = datetime.datetime.now(tz=EST5EDT()).time()

    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def getDay():
    return datetime.datetime.now(tz=EST5EDT()).strftime("%A")

class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)
        self.dston = d + datetime.timedelta(days=6 - d.weekday())
        d = datetime.datetime(dt.year, 11, 1)
        self.dstoff = d + datetime.timedelta(days=6 - d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'
