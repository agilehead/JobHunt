from django.http import HttpResponse, HttpResponseRedirect

from utils import dataplus
from website import models, codejar

def handle(request, format, user_id):
    if not request.user.is_authenticated(): return HttpResponseRedirect('/admin/')
    
    user = dataplus.returnIfExists(models.User.objects.filter(id=user_id))
    if user:    return codejar.user.downloadResume(user, format)
    else:       return HttpResponse('User does not exist.')
    