#!/usr/bin/env python
from django.db import models
from django.contrib import admin
from account import Account

ACTIVITY_TYPES = (
    ('UserReport', 'User Report'),
    ('SubResults', 'Subscription Results'),
    ('PropResults', 'Propaganda Results'),
    ('ProfEmailed', 'Profile Emailed'),
    ('ProfViewed', 'Profile Viewed'),
    ('ResumeRequest', 'Resume Request'),
    ('RecInvite', 'Recruiter Invite'),
)

class Notification(models.Model):
    key = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    text = models.TextField(null=True, blank=True)
    activity_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'Key: %s Type: %s' % (self.key, self.type)

    class Meta:
        app_label = 'website'

admin.site.register(Notification)