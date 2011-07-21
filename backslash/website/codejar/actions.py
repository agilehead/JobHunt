#!/usr/bin/env python
import cgi, datetime, string
from utils import dataplus, sysmessages
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from website import models
import auth

def addCookieToResponse(response, cookie_name, cookie_value,expiry_in_days=90):
    expiry_time = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=expiry_in_days), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(cookie_name, cookie_value, expires=expiry_time)
    return response

def handleSecurity(request, type):
    entity = {  'recruiter':auth.getLoggedInRecruiter,
                'user':auth.getLoggedInUser,
                'account':auth.getLoggedInAccount}[type](request)
    if entity:  return entity, None
    else:
        return_url = request.path
        query_string = request.GET.urlencode().replace('&','__amp__')
        if query_string:    return_url = return_url + '?' + query_string
        return None, HttpResponseRedirect('/login.htm?redir=' + return_url)
    
def redirectIfLoggedIn(request):
    account = auth.getLoggedInAccount(request)
    if account:
        if account.account_type == 'FR':    return HttpResponseRedirect('/recruiters/dashboard.htm')
        elif account.account_type == 'PU':    return HttpResponseRedirect('/dashboard.htm')
        else:   raise Exception('Invalid login state')

def render(request, html_file, dict=None, context=None):
    if not dict:    dict = {}
    account = auth.getLoggedInAccount(request)
    if account:
        dict['login_status'] = '<div id="loginStatus">\r\n<a href="/logout.htm">logout</a><br /> <span class="small">' + account.username + '</span>\r\n</div>'
    else:
        dict['login_status'] = '<div id="loginStatus">\r\n<a href="/login.htm">login</a>\r\n</div>'
    
    alerts = []
    if dict.has_key('flash_alerts'):    alerts = dict['flash_alerts']
    else:
        flash_id = dataplus.dictGetSafeVal(request.REQUEST, 'flashId','')
        if flash_id:    alerts = [sysmessages.getFlashMessage(flash_id)]
    if alerts:
        dict['py_scripts'] = '<script type="text/javascript">\n' + string.join(map(lambda x: 'alerts.register("' + x + '");', alerts), '\n') + '\n</script>\n'
    if context:
        return render_to_response(html_file, dict, context)
    else:
        return render_to_response(html_file, dict)        
    