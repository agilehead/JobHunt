from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from utils import dataplus
from website import codejar

def handle(request):    
    redirect = codejar.actions.redirectIfLoggedIn(request)
    if redirect:    return redirect
    
    if request.method in ['GET','HEAD']:
        return codejar.actions.render(request, 'index.htm')
    elif request.method == 'POST':
        if not (request.FILES):
            return HttpResponseRedirect('index.htm?flashId=upload_file_not_found')
        
        user_key, error_code = codejar.user.addFreeUserWithResume(request, 'resume_doc')
        if not user_key:
            return HttpResponseRedirect('index.htm?flashId=' + error_code)
        else:
            return HttpResponseRedirect('resumeactive.htm?key=' + user_key)
    else:
        return HttpResponseBadRequest()
