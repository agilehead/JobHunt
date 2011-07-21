#!/usr/bin/env python
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime, string, time
from utils import dataplus, i18n, mailer, config, eventnotifier, notifications
from website import models, codejar

def handle(request):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec:    return redirect

    recruiter_data = models.RecruiterData.objects.filter(recruiter=rec)[0]
    remaining_invites = recruiter_data.num_invites

    if request.method == 'GET':
        if remaining_invites == 0:
            eventnotifier.sendEventNotification('Recruiter %s with Id %s, has exhausted his invites' % (rec.name, rec.id))

        html, msg = getHTML(remaining_invites)
        return codejar.actions.render(request, 'recruiters/invites.htm',
                                      {'invite_message': msg,
                                       'email_boxes_html': html})

    elif request.method == 'POST':
        emails  = []
        if dataplus.dictGetSafeVal(request.REQUEST, 'email1'): emails.append(dataplus.dictGetSafeVal(request.REQUEST, 'email1').strip())
        if dataplus.dictGetSafeVal(request.REQUEST, 'email2'): emails.append(dataplus.dictGetSafeVal(request.REQUEST, 'email2').strip())
        if dataplus.dictGetSafeVal(request.REQUEST, 'email3'): emails.append(dataplus.dictGetSafeVal(request.REQUEST, 'email3').strip())
        if dataplus.dictGetSafeVal(request.REQUEST, 'email4'): emails.append(dataplus.dictGetSafeVal(request.REQUEST, 'email4').strip())
        if dataplus.dictGetSafeVal(request.REQUEST, 'email5'): emails.append(dataplus.dictGetSafeVal(request.REQUEST, 'email5').strip())

        if remaining_invites < 5:
            emails = emails[:remaining_invites]

        for email in emails:
            parameters = {'from': rec.name,
                          'token':models.Token.getNew(rec.account.id, email, 'Invites')}
            mailer.sendRecruiterInvites(email, parameters)
            eventnotifier.sendEventNotification('Recruiter %s(%s) has invited "%s"' % (rec.name, rec.email, email))

        remaining_invites = remaining_invites - len(emails)
        recruiter_data.num_invites = remaining_invites
        recruiter_data.save()

        if remaining_invites <= 0:
            eventnotifier.sendEventNotification('Recruiter %s with Id %s, has exhausted his invites' % (rec.name, rec.id))

        html, msg = getHTML(remaining_invites)
        return codejar.actions.render(request, 'recruiters/invites.htm',
                                      {'flash_alerts':['Invites have been sent. ' + msg],
                                       'email_boxes_html': html})

def getHTML(remaining_invites):
    html = ''
    if remaining_invites:
        html += '<table>'
        htmls = []
        for ctr in range(1,6):
            htmls.append("""<tr>
                                <td>
                                    %(ctr)d.
                                </td>
                                <td>
                                    <input id="email%(ctr)d" name="email%(ctr)d" type="text" size="32" class="full" />
                                </td>
                            </tr>""" % {'ctr':ctr})
        if remaining_invites < 5:
            htmls = htmls[:remaining_invites]

        for item in htmls:
            html += item

        html += '</table>'

    msg = ''
    if remaining_invites <= 0:
        msg = 'You will be receiving more invites shortly.'

    elif remaining_invites == 1:
        msg = 'You have ' + str(remaining_invites) + ' invite remaining.'

    else:
        msg = 'You have ' + str(remaining_invites) + ' invites remaining.'

    return html, msg
