#!/usr/bin/env python
from django.db import models
from django.contrib import admin

from recruiter import Recruiter

class RecruiterSubscription(models.Model):
    recruiter = models.ForeignKey(Recruiter, related_name='subscriptions')
    keywords = models.CharField(max_length=100)
    experience = models.IntegerField()
    location = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    max_salary = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)
    min_count = models.IntegerField(default=1)
    job_title = models.CharField(max_length=100, blank=True)
    job_company = models.CharField(max_length=100, blank=True)
    job_description = models.TextField(blank=True)

    results_last_sent_on = models.DateTimeField()

    def __unicode__(self):
        str = self.keywords.replace(', ', ',').replace(',', ', ')
        if self.experience: str += ' with %d years' % self.experience
        if not self.location.lower() == 'any':  str += ' in ' + self.location
        return str

    class Meta:
        app_label = 'website'

class RecruiterSubscriptionAdmin(admin.ModelAdmin):
    change_form_template = 'sys/filter_change_form.html'

admin.site.register(RecruiterSubscription, RecruiterSubscriptionAdmin)
