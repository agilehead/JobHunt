#!/usr/bin/env python
import datetime

def isToday(username):
##    todo: fetch the time diff from user record
    return lambda x: (datetime.datetime.utcnow() + datetime.timedelta(hours=5.5)).date() == (x + datetime.timedelta(hours=5.5)).date()

def toLocalTime(username):
##    todo: fetch the time diff from user record
    return lambda x: x + datetime.timedelta(hours=5.5)