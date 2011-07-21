from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import transaction

import datetime, re, string, time
from utils import dataplus, i18n, mailer, notifications
from website import models, codejar

def handle(request):
    token_value = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
    if token_value:
        token = dataplus.returnIfExists(models.Token.objects.filter(value=token_value))
    
    if not token:
        return HttpResponseRedirect('/?flashId=malformed_url')
        
    if request.method == 'GET':
        return codejar.actions.render(request, 'recruiters/signup.htm' , {'token': token})

    elif request.method == 'POST':
        name = dataplus.dictGetSafeVal(request.REQUEST, 'name', '').strip()
        email = dataplus.dictGetSafeVal(request.REQUEST, 'email', '').strip()
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '').strip()
        password2 = dataplus.dictGetSafeVal(request.REQUEST, 'password2', '').strip()
        organization = dataplus.dictGetSafeVal(request.REQUEST, 'organization', '').strip()
        telephone = dataplus.dictGetSafeVal(request.REQUEST, 'telephone', '').strip()

        errors = validateSignup(name, email, password, password2, telephone, organization)
        if not errors and dataplus.returnIfExists(models.Account.objects.filter(username=email)):
            errors.append('You already have an account with the same email.')

        if errors:
            return codejar.actions.render(request, 'recruiters/signup.htm', {'name':name, 'email':email, 'organization':organization,
                                                                'telephone':telephone, 'flash_alerts':errors})
        
        email_verified = (email == token.tag)
        rec = addRecruiter(email, password, name, organization, telephone, token, email_verified)
        subs = addDefaultSubscriptions(rec)
        
        #send activation email if sign up is not through an invite
        if not (email_verified):
            verify_token = models.Token.getNew(str(rec.account.id), email, 'VerifyEmail')
            params = {'recruiter_key':verify_token}
            mailer.sendActivationLink(email, params)
            
        return codejar.auth.login(request, email, password)

def validateSignup(name, email, password, password2, telephone, organization):
    re_email = re.compile('^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
    errors = []
    if len(name) < 3:    errors.append('Please provide your full name.')
    if not re_email.match(email): errors.append('Please provide a valid email.')
    if len(password) < 6: errors.append('Passwords should have minimum 6 characters.')
    elif not password == password2: errors.append('Passwords do not match.')
    if len(telephone) < 5: errors.append('Please provide a valid telephone.')
    if organization < 5: errors.append('Please provide the name of your organization.')
    return errors

def addDefaultSubscriptions(rec):
    min_date = datetime.datetime(1980, 10, 3)
    subs = []
    #Asp.Net subscription
    aspnet_sub = models.RecruiterSubscription(recruiter=rec, keywords='Asp.Net', experience=2, location='Any', industry='IT', max_salary=0, job_title='', job_company='', job_description='', results_last_sent_on=min_date)
    aspnet_sub.save()
    subs.append(aspnet_sub)
    #Java subscription
    #java_sub = models.RecruiterSubscription(recruiter=rec, keywords='Java', experience=2, location='Any', industry='IT', max_salary=0, job_title='', job_company='', job_description='', results_last_sent_on=min_date)
    #java_sub.save()
    #subs.append(java_sub)
    return subs

@transaction.commit_on_success
def addRecruiter(email, password, name, organization, telephone, token, through_invite):
    account = models.Account()
    account.username = email
    account.password = dataplus.hash(password)
    account.account_type = 'FR'
    account.account_state = 'A'
    
    account.email_verified = False
    if through_invite:
        account.email_verified = True
        
    account.save()

    rec = models.Recruiter()
    rec.account = account
    rec.key = dataplus.getUniqueId()

    rec.email = email
    rec.name = name
    rec.organization = organization
    rec.telephone = telephone

    #default values
    rec.verified = True #only through invites
    rec.verified_on = datetime.datetime(1981, 1, 9) #default date min value ;)
    rec.results_last_sent_on = datetime.datetime(1981, 1, 9)   #Jes' bday -- default min date

    rec.save()
    
    models.RecruiterData(recruiter=rec).save()
    
    #delete the token
    token.delete()

    return rec
