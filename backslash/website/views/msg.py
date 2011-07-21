from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from utils import dataplus, eventnotifier
from website import models, codejar

def handle(request):
    account, redirect = codejar.actions.handleSecurity(request, 'account')
    if request.method == 'GET': 
        msg_type = dataplus.dictGetSafeVal(request.REQUEST, 'type','contactus')
        
        msg_hdr = {'contactus': 'Contact us',
                    'bug': 'Bug Report',
                    'feedback': 'Feedback',
                    'suggestion': 'Suggestion',
                    'reportabuse': 'Report Abuse'}[msg_type]
        
        email = ''
        name = ''
        if account:
            email = account.username
            account_detail = models.User.objects.filter(account=account)
            if not account_detail:
                account_detail = models.Recruiter.objects.filter(account=account)
            name = account_detail[0].name
        
        return codejar.actions.render(request, 'msg.htm',
                                 {'msg_hdr':msg_hdr,
                                  'email':email,
                                  'name':name })
        
    elif request.method == 'POST':
        name = dataplus.dictGetSafeVal(request.REQUEST, 'name', '')
        email = dataplus.dictGetSafeVal(request.REQUEST, 'email', '')
        msg_hdr = dataplus.dictGetSafeVal(request.REQUEST, 'messageHeader', '')
        message = dataplus.dictGetSafeVal(request.REQUEST, 'message', '')
        
        eventnotifier.sendEventNotification("New Message: " + msg_hdr + " " + name + "(" + email + ")" + " says:\n" + message)
        
        return HttpResponseRedirect('thanks.html')
