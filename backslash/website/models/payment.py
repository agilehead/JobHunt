#!/usr/bin/env python
from django.db import models
from django.contrib import admin
from account import Account

class Payment(models.Model):
    account = models.ForeignKey(Account, related_name='payments')
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    payment_mode = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    success = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return  u'Payment %s - %s - %s' % (('Unconfirmed', 'Confirmed')[self.success], self.description, str(self.modified_at))
    
    class Meta:
        app_label = 'website'
        
    
admin.site.register(Payment)
