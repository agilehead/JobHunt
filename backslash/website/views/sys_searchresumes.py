from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response

import datetime, string
from utils import search_helper, dataplus
from website import models, codejar

def handle(request):
    filter_id = dataplus.dictGetSafeVal(request.REQUEST, 'filterId', '')
    if filter_id:
        resume_filter = get_object_or_404(models.RecruiterSubscription, id=filter_id)
        results = search_helper.matchResumes(resume_filter.keywords, resume_filter.experience, resume_filter.location, resume_filter.max_salary, resume_filter.added_on, datetime.datetime.utcnow())
        return HttpResponse(str(resume_filter) + ': Results(' + str(results) + ')')

    else:
        html = ''
        filters = models.RecruiterSubscription.objects.all()
        for resume_filter in filters:
            response = search_helper.matchResumes(resume_filter.keywords, resume_filter.experience, resume_filter.location, resume_filter.max_salary, resume_filter.added_on, datetime.datetime(1980,10,3))
            html += 'Results(' + str([result[id] for result in response.results]) + ')<br />'
        return HttpResponse(html)
