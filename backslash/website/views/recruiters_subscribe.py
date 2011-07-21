from django.http import HttpResponse, HttpResponseRedirect
import datetime, string
from website import models, codejar
from utils import dataplus, mailer, hotmetal

def handle(request):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec:     return redirect

    subscription_id = dataplus.dictGetSafeVal(request.REQUEST, 'subscriptionId')

    if request.method == 'GET':
        subscription = dataplus.returnIfExists(rec.subscriptions.filter(id=subscription_id))
        if (subscription):
            return codejar.actions.render(request, 'recruiters/subscribe.htm',
                {'subscription': subscription,
                 'experience_html':experienceHTML(subscription.experience),
                 'salary_html': salaryHTML(subscription.max_salary),
                 'location_html': locationHTML(subscription.location),
                 'subscriptionId': subscription_id})
        else:
            keywords = dataplus.dictGetSafeVal(request.REQUEST, 'keywords', '')
            experience = dataplus.dictGetVal(request.REQUEST, 'experience', '0', string.atoi)
            location = dataplus.dictGetSafeVal(request.REQUEST, 'location', '')
            max_salary = dataplus.dictGetVal(request.REQUEST, 'maxSalary', '0', string.atoi)
            return codejar.actions.render(request, 'recruiters/subscribe.htm',
                {'keywords':keywords,
                 'experience_html':experienceHTML(experience),
                 'salary_html': salaryHTML(max_salary),
                 'location_html': locationHTML(location)})

    elif request.method == 'POST':
        #Save the filter.
        def fillFormData(subs):
            subs.recruiter = rec
            subs.keywords = dataplus.dictGetSafeVal(request.REQUEST, 'keywords')
            subs.experience = dataplus.dictGetVal(request.REQUEST, 'experience', '0', string.atoi)
            subs.location = dataplus.dictGetSafeVal(request.REQUEST, 'location')
            subs.max_salary = dataplus.dictGetVal(request.REQUEST, 'maxSalary', '0', string.atoi)
            subs.job_title = dataplus.dictGetSafeVal(request.REQUEST, 'job_title')
            subs.job_company = dataplus.dictGetSafeVal(request.REQUEST, 'job_company')
            subs.job_description = dataplus.dictGetSafeVal(request.REQUEST, 'job_desc')

        if subscription_id:
            subscription = models.RecruiterSubscription.objects.get(id=subscription_id)
        else: #means new subscription
            subscription = models.RecruiterSubscription()
            subscription.min_count = 5
            subscription.industry = ''
            subscription.results_last_sent_on = datetime.datetime(1981, 1, 9) #Jes' bday - default min datetime

        fillFormData(subscription)
        subscription.save()

        return HttpResponseRedirect('/recruiters/dashboard.htm')

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
