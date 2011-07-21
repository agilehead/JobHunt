from django.http import HttpResponseRedirect
from utils import dataplus
from website import models, codejar

def handle(request):
    if codejar.auth.getLoggedInAccount(request):    codejar.auth.logout(request)
    
    if request.method == 'GET':
        redirect = codejar.actions.redirectIfLoggedIn(request)
        if redirect:    return redirect
        
        last_login = dataplus.dictGetSafeVal(request.COOKIES, 'last_login', '')
        
        return codejar.actions.render(request, 'login.htm', {'last_login':last_login})
    elif request.method == 'POST':
        email = dataplus.dictGetSafeVal(request.REQUEST, 'email', '')
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '')
        
        response = codejar.auth.login(request, email, password)
        return codejar.actions.addCookieToResponse(response, 'last_login', email)