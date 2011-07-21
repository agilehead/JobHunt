#!/usr/bin/env python
from django.http import HttpResponseRedirect

from website import models
from utils import dataplus

def login(request, username, password, success_url=''):
    account = dataplus.returnIfExists(models.Account.objects.filter(username=username, password=dataplus.hash(password)))
    redirect_url = '/login.htm?flashId=login_failed'
    if account and account.account_type in ['FR','PU']:
        request.session['username'] = account.username
        request.session['account_type'] = account.account_type
        request.session['account_state'] = account.account_state
        
        if success_url:
            redirect_url = success_url
        elif request.GET.get('redir',''):
            redirect_url = request.GET.get('redir','').replace('__amp__', '&')
        else:
            redirect_url = {'FR': '/recruiters/',
                            'PU':'/dashboard.htm'}[account.account_type]
                        
    return HttpResponseRedirect(redirect_url)

def logout(request):
    account_type = dataplus.dictGetVal(request.session, 'account_type', '')
    if account_type:
        request.session['username'] = None
        request.session['account_type'] = None
        
    return HttpResponseRedirect('/?flashId=logged_out')

def getLoggedInAccount(request):
    username = dataplus.dictGetVal(request.session, 'username', '')
    if username:
        return dataplus.returnIfExists(models.Account.objects.filter(username=username))
        
    ##Propaganda Special - if request has a valid 'rec_token' in querysting, we can login them.
    token_str = dataplus.dictGetSafeVal(request.REQUEST, 'rec_token', '')
    if token_str:
        rec_username = models.Token.getOwner(token_str)
        if rec_username:
            account = dataplus.returnIfExists(models.Account.objects.filter(username=rec_username, account_type='FR'))
            if account:
                request.session['username'] = account.username
                request.session['account_type'] = account.account_type
                request.session['account_state'] = account.account_state
                request.session['prop_login'] = True
                return account

def getLoggedInUser(request):
    account = getLoggedInAccount(request)
    if account and account.account_type == 'PU':
        return account.user
    
def getLoggedInRecruiter(request):
    account = getLoggedInAccount(request)
    if account and account.account_type == 'FR':
        return account.recruiter
    