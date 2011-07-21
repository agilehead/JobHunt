#!/usr/bin/env python
from django.db import models
from django.contrib import admin

import sys
sys.path.append('/websites/jobhuntin')
from utils import dataplus
import datetime

TOKEN_TYPES = (
    ('ForgotPassword', 'Forgot Password'),
    ('Invites', 'Invites'),
    ('VerifyEmail', 'Verify Email'),
    ('RecPropaganda', 'Recruiter Propaganda'),
)

class Token(models.Model):
    owner = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TOKEN_TYPES)
    tag = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def getNew(cls, owner, tag='', type='ForgotPassword'):
        token = Token()
        token.value = dataplus.getUniqueId()
        token.owner = owner
        token.tag = tag
        token.type = type
        
        token.save()
        return token.value
    
    @classmethod
    def getOwner(cls, token_value):
        token = dataplus.returnIfExists(Token.objects.filter(value=token_value))
        if token: return token.owner
    
    @classmethod
    def remove(cls, token_value):
        token = dataplus.returnIfExists(Token.objects.filter(value=token_value))
        if token : token.delete()

    def __unicode__(self):
        return u'owner: %s type: %s' % (self.owner, self.type)

    class Meta:
        app_label = 'website'

admin.site.register(Token)