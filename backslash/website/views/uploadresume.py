import datetime
from django.http import HttpResponse, HttpResponseRedirect
from utils import dataplus
from website import codejar

def handle(request):    
    user, redirect = codejar.actions.handleSecurity(request, 'user')
    if not user:    return redirect
    
    src = dataplus.dictGetVal(request.REQUEST, 'src', '')
    if request.method == 'GET':
        return codejar.actions.render(request, 'uploadresume.htm', {'src':src})
    
    elif request.method == 'POST':
        if not (request.FILES):
            return HttpResponseRedirect('uploadresume.htm?flashId=upload_file_not_found&src=' + src)
         
        filename, doc_filepath, error_id = codejar.user.saveUploadedResume(request, 'resume_doc')
        if not error_id:
            user.doc_filename = filename
            user.doc_filepath = doc_filepath
            user.resume_updated_on = datetime.datetime.utcnow()
            user.save()
            redirect_url = ('/dashboard.htm','/editprofile.htm')[src == 'editprofile']
            return HttpResponseRedirect(redirect_url + '?flashId=resume_uploaded')
        else:
            return HttpResponseRedirect('uploadresume.htm?flashId=' + error_id + '&src=' + src)