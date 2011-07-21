#!/usr/bin/env python
from django.db import models
from django.contrib import admin
from account import Account

class Recruiter(models.Model):
    account = models.OneToOneField(Account, related_name='recruiter')
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    verified = models.BooleanField()
    verified_on = models.DateTimeField()
    joined_date = models.DateTimeField(auto_now_add=True)
  
    def save(self):
        import sys
        sys.path.append('/websites/jobhuntin')
        from utils import eventnotifier
        if not self.id:
            eventnotifier.sendEventNotification('New Recruiter: ' + self.email)
        if self.verified and self.verified_on.year < 2000:
            from datetime import datetime
            self.verified_on = datetime.utcnow()
            self.account.account_state = 'A'
            
        if self.id > 0 and self.verified:
            rec = Recruiter.objects.get(id=self.id)
            if rec and not rec.verified:
                from jobs import recruiter_mail_job
                for sub in rec.subscriptions.all():
                    recruiter_mail_job.sendSubscriptionResults(sub, rec.id, rec.key, rec.email)
                
        super(Recruiter, self).save()
    
    def __unicode__(self):
        acct_state = {'A': 'Active',
                    'I': 'Inactive',
                    'D': 'Disabled',
                    'R': 'Removed'}[self.account.account_state]
        if not self.account.email_verified:
            return u'Email Not verified, %s: %s(%s) - %s' % (acct_state, self.name, self.email, self.organization)
        else:
            return u'%s,%s: %s(%s) - %s' % (('Pending Verification','Verified')[self.verified], acct_state, self.name, self.email, self.organization)

    class Meta:
        app_label = 'website'


admin.site.register(Recruiter)
