from django.http import HttpResponse, HttpResponseRedirect
from utils import dataplus, sysmessages, mailer
from website import models, codejar

def handle(request):
    if request.method == 'GET':
        return codejar.actions.render(request, 'forgotpassword.htm')
    elif request.method == 'POST':
        username = dataplus.dictGetSafeVal(request.REQUEST, 'email', '')
        account = dataplus.returnIfExists(models.Account.objects.filter(username=username))
        if account:
            account_detail = dataplus.returnIfExists(models.Recruiter.objects.filter(account=account))
            if not account_detail:
                account_detail = dataplus.returnIfExists(models.User.objects.filter(account=account))

            token = models.Token.getNew(str(account.id), account.username, 'ForgotPassword')
            params = {'account_key': token, 'path': {'FR':'/recruiters', 'PU':''}[account.account_type]}

            mailer.sendPasswordResetLink(username, params)
            return HttpResponseRedirect('?flashId=pwd_change_emailed')
        else:
            errors = []
            errors.append('Please provide the email that you used to register with us.')
            return codejar.actions.render(request, 'forgotpassword.htm',{'flash_alerts': errors})
