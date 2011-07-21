import string
from utils import dataplus
from website import models, codejar

def handle(request):
    user = codejar.auth.getLoggedInUser(request)
    if not user:    return codejar.ajaxian.getFailureResp('not_logged_in')

    section = dataplus.dictGetSafeVal(request.REQUEST, 'section', '')

    if section == 'jobInterest':
        user.is_job_hunting  = dataplus.dictGetSafeVal(request.REQUEST, 'is_job_hunting', '')

    elif section == 'personalPref':
        user.curr_designation = dataplus.dictGetSafeVal(request.REQUEST, 'curr_designation', '')
        user.curr_employer = dataplus.dictGetSafeVal(request.REQUEST, 'curr_employer', '')
        user.experience = dataplus.dictGetVal(request.REQUEST, 'experience', 0, string.atoi)
        user.tags = dataplus.dictGetSafeVal(request.REQUEST, 'tags', '')

    elif section == 'jobPref':
        user.min_salary = dataplus.dictGetVal(request.REQUEST, 'min_salary', 0, string.atoi)
        user.pref_designation = dataplus.dictGetSafeVal(request.REQUEST, 'pref_designation', '')
        user.pref_employment = dataplus.dictGetSafeVal(request.REQUEST, 'pref_employment', '')
        user.pref_location = dataplus.dictGetSafeVal(request.REQUEST, 'pref_location', '')

    elif section == 'summary':
        user.summary = dataplus.dictGetSafeVal(request.REQUEST, 'summary', '')
        user.settings_edited = True

    if user.name and user.email and user.tags and user.pref_location:    user.tagged = True

    user.save()

    return codejar.ajaxian.getSuccessResp(getUpdateHtml(user))

def getUpdateHtml(user):
    from website.views import dashboard
    from website.codejar import html_options
    htmlUpdate = {}
    htmlUpdate['display_update'] = dashboard.getSettingsDisplayHtml(user)
    htmlUpdate['edit_update'] = dashboard.getSettingsEditHtml(user)

    return htmlUpdate
