#!/usr/bin/env python
from django.db import models
from django.contrib import admin
from user import User
from recruiter import Recruiter
from recruiter_subscription import RecruiterSubscription

class RecruiterMailLog(models.Model):
    recruiter = models.ForeignKey(Recruiter, related_name='received_users')
    user = models.ForeignKey(User, related_name='sent_recruiters')
    subscription = models.ForeignKey(RecruiterSubscription, related_name='emailed_users')
    sent_on = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return u'Recruiter: %s' % (self.recruiter)

    class Meta:
        app_label = 'website'

admin.site.register(RecruiterMailLog)