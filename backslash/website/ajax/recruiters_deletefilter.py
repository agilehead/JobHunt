import string
from utils import dataplus
from website import models, codejar

def handle(request):
    try:
        rec = codejar.auth.getLoggedInRecruiter(request)
        if rec:
            id = dataplus.dictGetVal(request.REQUEST, 'filterId', 0, string.atoi)
            filter = models.RecruiterSubscription.objects.filter(recruiter=rec, id=id)
            if filter:  filter.delete()
            return codejar.ajaxian.getSuccessResp('')
        else:
            return codejar.ajaxian.getFailureResp('not_logged_in')
    except:
        return codejar.ajaxian.getFailureResp()
