#!/usr/bin/env python
from django.db import models
from django.contrib import admin

class TellFriend(models.Model):
    sender_name = models.CharField(max_length=100)
    receiver_email = models.CharField(max_length=100)
    message = models.TextField()
    ip_address = models.CharField(max_length=20)
    requested_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField()
    sent = models.BooleanField()
    
    def __unicode__(self):
        return  u'%s - %s - %s - %s - %s' % (('Unsent','Sent')[self.sent], self.ip_address, str(self.requested_at), self.sender_name, self.receiver_email)
    
    def save(self):
        if self.verified and not self.sent:
            import sys
            sys.path.append('/websites/jobhuntin')
            from utils import mailer
            mailer.sendInviteFriend(self)
            self.sent = True
        super(TellFriend, self).save()

    class Meta:
        app_label = 'website'

admin.site.register(TellFriend)