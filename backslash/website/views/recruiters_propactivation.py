#!/usr/bin/env python
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction

import datetime, re, string, time
from utils import dataplus, i18n, mailer, notifications
from website import models, codejar

def handle(request):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec:    return redirect
    
    if request.method == 'GET':
        token = models.Token.getNew(str(rec.account.id), rec.account.username, 'ForgotPassword')
        params = {'account_key': token, 'path': '/recruiters'}
    
        mailer.sendPasswordResetLink(rec.account.username, params)
        return codejar.actions.render(request, 'recruiters/propactivation.htm',
                {'rec_email':rec.email})
            

