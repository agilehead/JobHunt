from django.http import HttpResponseRedirect
import string
from utils import dataplus
from website import models, codejar

def handle(request):
    user_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
    from_email = dataplus.dictGetVal(request.REQUEST, 'source', False, lambda x: x == 'email')
    user = dataplus.returnIfExists(models.User.objects.filter(key=user_key))
    if not user:
        return codejar.actions.render(request, 'info.htm', {'info_header':'Resume not found',
                                                            'info_text':'This resume does not exist,<br /> or may have been deleted.'})
    
    if request.method == 'GET':
        return codejar.actions.render(request, 'resumeactive.htm', {'user_key':user_key,'from_email':from_email})
    elif request.method == 'POST':
        user.min_salary = dataplus.dictGetVal(request.REQUEST, 'minSalary', 0, string.atoi)
        user.pref_employer = dataplus.dictGetSafeVal(request.REQUEST, 'preferredEmployer', '')
        user.pref_location = dataplus.dictGetSafeVal(request.REQUEST, 'preferredLocations', '')
        user.save()
        return HttpResponseRedirect('done.html')