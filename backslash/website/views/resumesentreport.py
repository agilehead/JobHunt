#!/usr/bin/env python
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response

import cPickle, cgi, datetime, string
from utils import dataplus
from website import models, codejar

def handle(request):
    user, redirect = codejar.actions.handleSecurity(request, 'user')
    if not user:	return redirect
    
    if request.method == 'GET':
        #YYYYMMDD
        report_date = dataplus.dictGetVal(request.REQUEST, 'date', None, lambda x: datetime.datetime.strptime(x, '%Y%m%d'))
        if not report_date:
            return HttpResponseRedirect('/?flashId=malformed_url')
        
        notification = dataplus.returnIfExists(models.Notification.objects.filter(key=str(user.id), type='UserReport', activity_time__year=report_date.year,
                                                                             activity_time__month = report_date.month,
                                                                             activity_time__day = report_date.day))
        if not notification:
            return HttpResponseRedirect('/?flashId=malformed_url')
        
        context = cPickle.loads(str(notification.text))
        return codejar.actions.render(request, 'resumesentreport.htm',
                                      {'recruiter_infos':context['recruiter_infos'],
                                       'num_of_sends': context['num_of_sends'],
                                       'date': report_date})
    elif request.method == 'POST':
        pass
    


