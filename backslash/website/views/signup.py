from django.http import HttpResponseRedirect
import re, string
from utils import dataplus
from website import models, codejar

def handle(request):    
    if request.method == 'GET':
        return codejar.actions.render(request, 'signup.htm')
        
    elif request.method == 'POST':
        name = dataplus.dictGetSafeVal(request.REQUEST, 'name', '').strip()
        email = dataplus.dictGetSafeVal(request.REQUEST, 'email', '').strip()
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '').strip()
        password2 = dataplus.dictGetSafeVal(request.REQUEST, 'password2', '').strip()
        telephone = dataplus.dictGetSafeVal(request.REQUEST, 'telephone', '').strip()
        
        errors = validateSignup(name, email, password, password2, telephone)
        if not errors and dataplus.returnIfExists(models.Account.objects.filter(username=email)):
            errors.append('You already have an account with the same email.')
            
        if errors:
            return codejar.actions.render(request, 'signup.htm', {'name':name, 'email':email, 'telephone':telephone,
                                                                'flash_alerts':errors})
        else:
            user = codejar.user.addPremiumUser(name, email, password, telephone)
            return codejar.auth.login(request, email, password)

def validateSignup(name, email, password, password2, telephone):
    re_email = re.compile('^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
    errors = []
    if len(name) < 3:    errors.append('Please provide your full name.')
    if not re_email.match(email): errors.append('Please provide a valid email.')
    if len(password) < 6: errors.append('Passwords should have minimum 6 characters.')
    elif not password == password2: errors.append('Passwords do not match.')
    if len(telephone) < 5: errors.append('Please provide a valid telephone.')
    
    return errors
    