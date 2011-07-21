from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

import datetime, re, string, time
from utils import dataplus, i18n
from website import models, codejar

def handle(request):
    rec = codejar.auth.getLoggedInRecruiter(request)
    if not rec: return HttpResponseRedirect('/login.htm')

    if request.method == 'GET':
        return codejar.actions.render(request, 'recruiters/settings.htm',
                                 {'telephone':rec.telephone})

    elif request.method == 'POST':
        telephone = dataplus.dictGetSafeVal(request.REQUEST, 'telephone', '').strip()
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '').strip()
        password2 = dataplus.dictGetSafeVal(request.REQUEST, 'password2', '').strip()


        errors = validateSignup(telephone, password, password2)
        if errors:
            flash_message = '<ul>\n' + string.join(['<li>' + x + '</li>' for x in errors], '\n') + '</ul>\n'
            return codejar.actions.render(request, 'recruiters/settings.htm', {'telephone':telephone, 'flash_message':flash_message})
        else:
            if password != '' and password2 != '':
                rec.password = password
            rec.telephone = telephone
            rec.save()
            return HttpResponseRedirect('dashboard.htm')

def validateSignup(telephone, password, password2):
    re_email = re.compile('^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
    errors = []
    if password != '' and password2 != '':
        if len(password) < 8: errors.append('Passwords should have minimum 8 characters.')
        elif not password == password2: errors.append('Passwords do not match.')
        if len(telephone) < 5: errors.append('Please provide a valid telephone.')

    return errors
