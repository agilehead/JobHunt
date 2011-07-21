#!/usr/bin/env python
from django.db import models
from django.contrib import admin

class ReceivedMail(models.Model):
    from_address = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body_html = models.TextField()
    body_text = models.TextField()
    doc_filepath = models.CharField(max_length=100, blank=True)
    received_on = models.DateTimeField()
    
    def __unicode__(self):
        return  u'%s (%s)' % (self.from_address, self.subject)

    class Meta:
        app_label = 'website'

admin.site.register(ReceivedMail)