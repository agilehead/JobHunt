from utils import dataplus, notifications
from website import models, codejar

from django.http import Http404

def handle(request):
    try:
        rec = codejar.auth.getLoggedInRecruiter(request)
        if rec:
            user_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
            user = dataplus.returnIfExists(models.User.objects.filter(key=user_key))
            
            notifications.addNotification(user.id, 'ResumeRequest', data={'recruiter_id':rec.id})
            return codejar.ajaxian.getSuccessResp('')
        else:
            return codejar.ajaxian.getFailureResp('not_logged_in')
    except:
        return codejar.ajaxian.getFailureResp('')
