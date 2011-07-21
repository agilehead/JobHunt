#!/usr/bin/env python
from django.db import models
from django.contrib import admin

class IndexDelta(models.Model):
    user_id = models.IntegerField(unique=True)
    index_type = models.CharField(max_length=20)
    marked_at = models.DateTimeField(auto_now=True)
    
    def save(self):
        if not self.id:
            entries = IndexDelta.objects.filter(user_id=self.user_id)
            if entries:
                entry = entries[0]
                entry.index_type = self.index_type
                entry.save()
                return
        
        super(IndexDelta, self).save()
    
    def __unicode__(self):
        return u'User id: %s Index-Type: %s' % (self.user_id, self.index_type)

    class Meta:
        app_label = 'website'

admin.site.register(IndexDelta)