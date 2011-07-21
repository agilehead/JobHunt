from django.http import HttpResponse, HttpResponseRedirect, Http404
import cPickle, datetime, string, time
from utils import dataplus, hotmetal, mailer, eventnotifier
from website import models, codejar

def handle(request):
    if request.method == 'GET':
        rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
        if not rec:    return redirect
        
        #Propaganda special
        is_prop_login = dataplus.dictGetVal(request.session, 'prop_login', False)
        if is_prop_login:
            account_state = dataplus.dictGetVal(request.session, 'account_state', 'I')
            if account_state == 'I':
                if rec.account.account_state == 'I':
                    rec.account.account_state = 'A'
                    rec.account.save()
                    eventnotifier.sendEventNotification('Recruiter PropActivated: ' + rec.email)

            elif account_state == 'A':
                return HttpResponseRedirect('propactivation.htm')
        

        recent_searches = models.RecruiterData.getRecentSearches(rec)
        recent_searches_formatted = []
        for dict in recent_searches:
            dict['keywords'] = dict['keywords'].replace(', ', ',').replace(',', ', ')
            json_dict = u"{'keywords':'%s', 'experience':'%d', 'location':'%s', 'max_salary':'%d'}" % (dict['keywords'], dict['experience'], dict['location'], dict['max_salary'])
            display_str = dict['keywords']
            if dict['experience'] > 0:  display_str += u" with %d years" % (dict['experience'])
            if not dict['location'].lower() == 'any':   display_str += u" in " + dict['location']
            recent_searches_formatted.append((display_str, json_dict))

        return codejar.actions.render(request, 'recruiters/dashboard.htm',
                {'experience_html':experienceHTML(),
                 'salary_html': salaryHTML(),
                 'location_html': locationHTML(),
                 'recent_searches': recent_searches_formatted,
                 'recent_subscriptions': [str(subscr) for subscr in rec.subscriptions.order_by('-added_on')[:2]],
                 'email_verified': rec.account.email_verified })

    elif request.method == 'POST':
##      shouldn't be happening :)
        pass

def experienceHTML(selectVal=0):
    html = hotmetal.elemSelect([('Any','0')], (1,2,5,10), lambda x: str(x) + ' years', lambda x: x,
                                selectVal, 'name="experience" id="experience"')
    return html

def locationHTML(selectVal='Any'):
    locations = ('Bangalore','Chennai','Hyderabad','NCR','Kolkata','Pune','Mumbai','Andhra Pradesh','Arunachal Pradesh',
                'Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir',
                'Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland',
                'Orissa','Punjab','Rajasthan','Sikkim','Tamil Nadu','Tripura','Uttar Pradesh','Uttarakhand','West Bengal')
    html = hotmetal.elemSelect([('Any','Any')], locations, lambda x:x, lambda x:x,
                                selectVal, 'name="location" id="location"')
    return html

def salaryHTML(selectVal=0):
    salary = (200000, 400000, 600000, 1000000, 2000000)
    html = hotmetal.elemSelect([('No Limit','0')], salary, lambda x: str(x)[:-5] + ' Lakhs', lambda x: x,
                                selectVal, 'name="maxSalary" id="maxSalary"')
    return html
