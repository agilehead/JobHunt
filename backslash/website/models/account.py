#!/usr/bin/env python
import sys
from django.db import models

sys.path.append('/websites/jobhuntin')
from utils import dataplus

ACCOUNT_TYPES = (
    ('FU', 'Free User'),
    ('PU', 'Premium User'),
    ('FR', 'Free Recruiter'),
##    ('PR', 'Premium Recruiter'),
)

ACCOUNT_STATES = (
    ('A', 'Active'),
    ('I', 'Inactive'),
    ('D', 'Disabled'),
    ('R', 'Removed'),
)

class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=32)
    email_verified = models.BooleanField()
    account_type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
    account_state = models.CharField(max_length=2, choices=ACCOUNT_STATES)
    
    @classmethod
    def create(cls, username, password, account_type):
        acct = Account(username=username, password=dataplus.hash(password), account_type=account_type, account_state='A', email_verified=False)
        acct.save()
        
        return acct

    def setPassword(self, new_password):
        self.password = dataplus.hash(new_password)
        self.save()
    
    def __unicode__(self):
        return u'%s' % (self.username)

    class Meta:
        app_label = 'website'

from django.contrib import admin
admin.site.register(Account)
