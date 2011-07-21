from utils import mailer, dataplus
from website import models, codejar

from django.http import Http404

def handle(request):
    try:
        rec = codejar.auth.getLoggedInRecruiter(request)
        if rec:
            token = dataplus.returnIfExists(models.Token.objects.filter(owner=rec.email, type='VerifyEmail'))
            if not token:
                token = models.Token.getNew(rec.account.id, rec.email, 'VerifyEmail')
            else:
                token = token.value
            params = {'recruiter_key':token}
            mailer.sendActivationLink(rec.email, params)
            return codejar.ajaxian.getSuccessResp(True)
        else:
            return codejar.ajaxian.getFailureResp('not_logged_in')
    except:
        return codejar.ajaxian.getFailureResp('')
