from django.http import Http404
from django.shortcuts import get_object_or_404
import website.models as models
from utils import dataplus, notifications
from website import codejar

def handle(request, format, user_key):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec:
        rec_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
        if rec_key: rec = dataplus.returnIfExists(models.Recruiter.object.filter(key=rec_key))        
    if not rec: return redirect
    
    user = get_object_or_404(models.User, key=user_key)    
    if not format in ('doc', 'html'): 
		format = 'doc'
    
    sub_id = dataplus.dictGetVal(request.REQUEST, 'sub_id', 0)
    notifications.addNotification(str(user.id), 'ProfViewed', data={'recruiter_id': rec.id, 'subscription_id':sub_id})
    
    return codejar.user.downloadResume(user, format)
