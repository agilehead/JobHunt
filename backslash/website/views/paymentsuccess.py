import string
from django.http import Http404, HttpResponseRedirect
from utils import dataplus, mailer
from website import models, codejar

def handle(request, account_type='user'):
    if request.method == 'GET':
        order_id = request.session['Order_Id']
        pymt = dataplus.returnIfExists(models.Payment.objects.filter(order_id=order_id))
        if pymt:
            account = dataplus.returnIfExists(models.Account.objects.filter(id=pymt.account.id))
            account.account_state = 'A'
            account.save()
            mailer.sendAnonUserWelcomeMail(account.username, {'username':account.username})
            request.session['username'] = account.username
            request.session['account_type'] = account.account_type
            request.session['account_state'] = account.account_state
            request.session['Order_Id'] = None
            return HttpResponseRedirect('/dashboard.htm?flashId=welcome_user')
        
        else:
            raise Http404