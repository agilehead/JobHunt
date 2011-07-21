from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime, string, time
from utils import dataplus, i18n, mailer
from website import models, codejar

def handle(request):
    if request.method == 'GET':
        rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
        if not rec:    return redirect

        def addDateFuncs(x):
            x.isToday = i18n.isToday(rec.email)(x.added_on)
            x.added_on_localTime = i18n.toLocalTime(rec.email)(x.added_on)
            return x

        filters = map(addDateFuncs, rec.subscriptions.all())

        for f in filters:
            salary_text = '-'
            if f.max_salary:
                salary_text = "%dL" % (f.max_salary/100000)
            f.max_salary_display = salary_text

        return codejar.actions.render(request, 'recruiters/subscriptions.htm',
                {'recruiter_key':rec.key,
                'filters':filters,
                'email_verified': rec.account.email_verified})

    elif request.method == 'POST':
##      shouldn't be happening :)
        pass
