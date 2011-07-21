from django.http import HttpResponse, HttpResponseRedirect

from utils import dataplus, mailer, notifications, search_helper
from website import models, codejar
import datetime, random, re, string

def handle(request):
    if not request.user.is_authenticated(): return HttpResponseRedirect('/admin/')
    
    if request.method == 'GET':
        return codejar.actions.render(request, 'sys/recinvite.htm')
    
    elif request.method == 'POST':
        rec_emails = dataplus.dictGetSafeVal(request.REQUEST, 'emails', '')
        keywords = dataplus.dictGetSafeVal(request.REQUEST, 'keywords', '')
        experience = dataplus.dictGetVal(request.REQUEST, 'experience', 0, string.atoi)
        location = dataplus.dictGetSafeVal(request.REQUEST, 'location', '')
        key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
        if rec_emails:
            min_datetime = datetime.datetime(1980, 10, 3)   #min_date
            response = search_helper.matchResumes(keywords, experience, location, 99999999, min_datetime)
            usr_list = response.results
            usr_list.sort(lambda x,y: x['rating']-y['rating'])
            usr_list = addFormatting(usr_list[:50])
            
            for email in rec_emails.split(','):
                token_value = models.Token.getNew('system', email, 'Invites')
                sel_users = getRandomUsers(usr_list)
                for usr in sel_users:
                    notifications.addNotification(usr['id'], 'ProfEmailed', data={'recruiter_email':email})
                mailer.sendAdminRecruiterInvites(email, {'token':token_value, 'key':key, 'matching_users':sel_users})
        
        return HttpResponseRedirect('/sys/recinvite.htm?flashId=recruiters_invited')

def addFormatting(users):
    for usr in users:
        min_salary_desc = ''
        if usr['min_salary']:    usr['min_salary'] = '%d Lakhs' % (usr['min_salary']/100000)
        #Software Engineer with Helzinger Consulting, 7 years exp, in Bangalore.
        usr['profile_info'] = ('Fresher', "%s with %s, %d years of experience." % (usr['curr_designation'], usr['curr_employer'], usr['experience']))[usr['experience'] > 0]

        if usr['summary']:
            summary_html =  string.join([x.strip() for x in re.split('\n+', re.sub('\r?\n', '\n', usr['summary'])) if re.match('[a-zA-Z]{2,}', x.strip())], ' <strong> | </strong> ') + '.'
            if len(summary_html) > 300: summary_html = summary_html[:297] +'...'
            if summary_html.rfind('<strong>') > summary_html.rfind('</strong>'):   summary_html = summary_html[:summary_html.rfind('<strong>')].strip() + '...'
            usr['summary'] = summary_html
        usr['is_premium_user'] = (usr['account_type'] == 'PU')

    return users

def getRandomUsers(user_list, count=10):
    new_list = []
    if user_list <= count:  return user_list
    
    while len(new_list) < count:
        val = user_list[random.randint(0,0xffffff) % len(user_list)]
        if not val in new_list: new_list.append(val)
    
    return new_list
        