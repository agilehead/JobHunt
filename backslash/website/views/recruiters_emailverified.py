from django.http import HttpResponseRedirect, Http404

from website import models, codejar
from utils import dataplus

def handle(request):
    if request.method == 'GET':
        key = dataplus.dictGetSafeVal(request.REQUEST, 'key', 'NotFound')
        rec_acct_id = models.Token.getOwner(key)
        rec = dataplus.returnIfExists(models.Recruiter.objects.filter(account__id=rec_acct_id))
        if not rec: return HttpResponseRedirect('/?flashId=malformed_url')
        
        rec.account.email_verified = True
        rec.account.save()

        models.Token.remove(key)
        
        return codejar.actions.render(request, 'recruiters/emailverified.htm')
        
    elif request.method == 'POST':
        pass