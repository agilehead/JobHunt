from django.http import HttpResponseRedirect
from utils import dataplus

def handle(request):
    resume_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
    return HttpResponseRedirect('resumeactive.htm?key='+resume_key+'&source=email')