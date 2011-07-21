from django.http import HttpResponse, HttpResponseRedirect

import string
from utils import dataplus, mailer, notifications
from website import models, codejar
from website.codejar import html_options

def handle(request, account_type='user'):
    rec = None
    if account_type == 'user':
        user, redirect = codejar.actions.handleSecurity(request, 'user')
        if not user:    return redirect
    elif account_type == 'recruiter':
        rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
        if not rec:     return redirect
        user_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
        user = dataplus.returnIfExists(models.User.objects.filter(key=user_key))
        if not user:    return codejar.actions.render(request, 'error.htm', {'error_message':'You have entered an invalid Url. Please check and try again.'})
        
    if request.method == 'GET':
        pref_summary = ''
        #12 Lakhs, Large Companies only, in Bangalore.
        if user.pref_designation and user.min_salary and user.pref_location and user.pref_employment:
            pref_summary = '%s in %s' % (user.pref_designation, html_options.getVerboseEmploymentType(user.pref_employment))
            if not user.pref_location == 'Anywhere':    pref_summary += ', in ' + user.pref_location
        
        user.job_preferences = pref_summary
        if user.summary:
            user.summary_display = '<ul>\n' + reduce(lambda x,y: x + '<li>' + y + '</li>\n', user.summary.split('\n'), '') + '</ul>\n'

        user.min_salary_in_lakhs = user.min_salary/100000
        
        if rec:
            sub_id = dataplus.dictGetVal(request.REQUEST, 'sub_id', 0, string.atoi)
            notifications.addNotification(str(user.id), 'ProfViewed', data={'recruiter_id': rec.id, 'subscription_id':sub_id})
        return codejar.actions.render(request, 'viewsummary.htm', {'user':user, 'rec':rec})
    elif request.method == 'POST':
        pass
