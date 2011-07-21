from django.db import models
from django.contrib import admin
from recruiter import Recruiter

import cPickle

class RecruiterData(models.Model):
    recruiter = models.OneToOneField(Recruiter, related_name='data')
    num_invites = models.IntegerField(default=10)
    recent_searches = models.TextField(max_length=500, blank=True, null=True)
    
    @classmethod
    def addToRecentSearches(cls, recruiter, search_dict):
        data = RecruiterData.objects.get(recruiter=recruiter)
        recent_searches = []
        if data.recent_searches:    recent_searches = cPickle.loads(str(data.recent_searches))
        if search_dict in recent_searches:
            recent_searches.remove(search_dict)
        else:
            if len(recent_searches) == 5:    recent_searches = recent_searches[1:]
            
        recent_searches.append(search_dict)
        data.recent_searches = cPickle.dumps(recent_searches)
        data.save()
    
    @classmethod
    def getRecentSearches(cls, recruiter):
        data = RecruiterData.objects.get(recruiter=recruiter)
        recent_searches = []
        if data.recent_searches:    recent_searches = cPickle.loads(str(data.recent_searches))
        recent_searches.reverse()
        return recent_searches
    
    def __unicode__(self):
        return u'Recruiter: %s' % (self.recruiter)
    
    class Meta:
        app_label = 'website'

admin.site.register(RecruiterData)