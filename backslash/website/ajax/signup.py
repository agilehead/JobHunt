import re, string
from utils import dataplus
from website import models, codejar

def handle(request):
    try:
        name = dataplus.dictGetSafeVal(request.REQUEST, 'name', '').strip()
        email = dataplus.dictGetSafeVal(request.REQUEST, 'email', '').strip()
        password = dataplus.dictGetSafeVal(request.REQUEST, 'password', '').strip()
        password2 = dataplus.dictGetSafeVal(request.REQUEST, 'password2', '').strip()
        telephone = dataplus.dictGetSafeVal(request.REQUEST, 'telephone', '').strip()
        
        errors = validateSignup(name, email, password, password2, telephone)
        if not errors and dataplus.returnIfExists(models.Account.objects.filter(username=email)):
            errors.append('You already have an account with the same email.')
            
        if errors:
            return codejar.ajaxian.getFailureResp(errors)
        else:
            user = codejar.user.addPremiumUser(name, email, password, telephone)
            pymt = models.Payment(account=user.account, amount=200, payment_mode='CCAvenue', description='Premium User account subscription')
            pymt.order_id = dataplus.getNewOrderId()
            pymt.save()
            request.session['Order_Id'] = pymt.order_id
            return codejar.ajaxian.getSuccessResp(pymt.order_id)
    except:
        return codejar.ajaxian.getFailureResp('')

def validateSignup(name, email, password, password2, telephone):
    re_email = re.compile('^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$')
    errors = []
    if len(name) < 3:    errors.append('Please provide your full name.')
    if not re_email.match(email): errors.append('Please provide a valid email.')
    if len(password) < 6: errors.append('Passwords should have minimum 6 characters.')
    elif not password == password2: errors.append('Passwords do not match.')
    if len(telephone) < 5: errors.append('Please provide a valid telephone.')
    
    return errors
