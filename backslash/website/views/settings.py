from django.http import HttpResponse, HttpResponseRedirect
from utils import dataplus
from website import codejar

def handle(request):    
    user, redirect = codejar.actions.handleSecurity(request, 'user')
    if not user:    return redirect
    
    if request.method == 'GET':
        return codejar.actions.render(request, 'settings.htm')
    
    elif request.method == 'POST':
        raise Exception('Invalid request method')