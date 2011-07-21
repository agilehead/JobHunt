from django.http import Http404
from django.shortcuts import get_object_or_404
from website import models, codejar
from utils import dataplus

def handle(request):
    user, redirect = codejar.actions.handleSecurity(request, 'user')
    if not user:    return redirect
    
    format = dataplus.dictGetSafeVal(request.REQUEST, 'format', '')
    if not format in ('doc', 'html'): raise Http404
    
    return codejar.user.downloadResume(user, format)