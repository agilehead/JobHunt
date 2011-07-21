from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from utils import dataplus, eventnotifier, mailman, search_helper
from website import models, codejar
import string, cPickle, base64, datetime

def handle(request):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec: return redirect
    
    email_list = dataplus.dictGetSafeVal(request.REQUEST, 'email_list', '')
    email_query = dataplus.dictGetSafeVal(request.REQUEST, 'email_query', '')
    if email_query:
        search_keywords, experience, location, max_salary = cPickle.loads(base64.b64decode(email_query))
        response = search_helper.matchResumes(search_keywords, experience, location, max_salary, datetime.datetime(1981, 1, 9))
        email_list = dataplus.decode(string.join([usr['email'] for usr in response.results], '; '))
    
    action = dataplus.dictGetSafeVal(request.REQUEST, 'action', '')
    if action == 'show_form':
        return codejar.actions.render(request, 'recruiters/emailusers.htm',
                               {'to_list':email_list,
                                'recruiter': rec})
    
    elif action == 'email_users':
        subject = dataplus.dictGetSafeVal(request.REQUEST, 'subject', '')
        message = dataplus.dictGetSafeVal(request.REQUEST, 'message', '')
        
        message += '<p>&nbsp;</p><div style="border-bottom: 1px solid rgb(153, 153, 153);"></div><p>This email has been sent by %s(%s) of %s using <a href="http://www.jobhunt.in">www.jobhunt.in</a> services.</p>' % (rec.name, rec.email, rec.organization)
        mailman.sendMail(rec.name + '<mailman@jobhunt.in>', email_list.split(';'), subject, message, reply_to=rec.email)
        
        eventnotifier.sendEventNotification("New Recruiter Mass Mail: " + subject + " - " + rec.name + "(" + rec.email + ")" + " message:\n" + message)
        
        return HttpResponseRedirect('dashboard.htm?flashId=email_sent')
