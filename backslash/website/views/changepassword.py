import string
from django.http import HttpResponse, HttpResponseRedirect
from utils import dataplus
from website import models, codejar

def handle(request, account_type='user'):
    account, redirect = codejar.actions.handleSecurity(request, 'account')
    token_value = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')

    url_prefix = ''
    if account_type == 'recruiters':
        url_prefix = 'recruiters/'

    if request.method == 'GET':
        return codejar.actions.render(request, url_prefix + 'changepassword.htm', {'key':token_value, 'is_loggedin': ('true', '')[account is None]})

    elif request.method == 'POST':
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '')
        password2 = dataplus.dictGetSafeVal(request.REQUEST, 'password2', '')
        errors = []
        if len(password) < 6: errors.append('Passwords should have minimum 6 characters.')
        elif not password == password2: errors.append('Passwords do not match.')

        if errors:
            flash_alerts = errors
            return codejar.actions.render(request, url_prefix + 'changepassword.htm', {'flash_alerts':flash_alerts})


        if not account:
            acct_id = string.atoi(models.Token.getOwner(token_value))
            account = dataplus.returnIfExists(models.Account.objects.filter(id=acct_id))
            
            if not account:                
                return HttpResponseRedirect('/?flashId=malformed_url')

        account.setPassword(password)

        #Propaganda special
        if dataplus.dictGetVal(request.session, 'prop_login', False):
            request.session['prop_login'] = None
            prop_token = dataplus.returnIfExists(models.Token.objects.filter(owner=account.username, type='RecPropaganda'))
            if prop_token:  prop_token.delete()

        if token_value:
            models.Token.remove(token_value)
            response = codejar.auth.login(request, account.username, password, 'dashboard.htm?flashId=password_changed')
            return codejar.actions.addCookieToResponse(response, 'last_login', account.username)
        else:
            return HttpResponseRedirect('dashboard.htm?flashId=password_changed')
