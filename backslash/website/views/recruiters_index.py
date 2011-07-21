from django.http import HttpResponseRedirect

def handle(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/recruiters/dashboard.htm')