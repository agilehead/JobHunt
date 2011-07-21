#!/usr/bin/env python
import django_templater, mailman
import datetime, re
from string import Template

def sendNewFilterAddedMail(to_email, parameters):
    subject = "New subscription added"
    sendWithTemplate(to_email, subject, parameters, 'rec_new_subscription.html', 'rec_new_subscription.txt')

def sendResumeAddedMail(to_email, parameters):
    subject = "Your resume is added"
    sendWithTemplate(to_email, subject, parameters, 'resumeadded.html', 'resumeadded.txt')

def sendResumeUpdatedMail(to_email, parameters):
    subject = "Your resume is updated"
    sendWithTemplate(to_email, subject, parameters, 'resumeupdated.html', 'resumeupdated.txt')

def sendPremiumUserLoginToUpdateAlert(to_email, parameters=None, by_mail=False):
    if not parameters:  parameters={}
    subject = "Please login to update your resume"
    sendWithTemplate(to_email, subject, parameters, 'puinvalidresume.html', 'puinvalidresume.txt')

def sendResumeReceivedMail(to_email, parameters):
    subject = "Got your resume"
    sendWithTemplate(to_email, subject, parameters, 'gotmail.html', 'gotmail.txt')

def sendInvalidResumeMail(to_email, parameters):
    subject = "Problem with your resume"
    sendWithTemplate(to_email, subject, parameters, 'invalidmail.html', 'invalidmail.txt')

def sendRecruiterVerifiedMail(to_email, parameters):
    subject = "Your account is activated"
    sendWithTemplate(to_email, subject, parameters, 'recruiterverified.html', 'recruiterverified.txt')

def sendInviteFriend(friend_request):
    params = {'inviter':friend_request.sender_name.split()[0],
            'date': datetime.datetime.utcnow().strftime('%B%e, %Y'),
            'message': friend_request.message,
            'message_html': friend_request.message.replace('\n','<br />')}
    subject = friend_request.sender_name + ' thinks you should see jobhunt.in'
    sendWithTemplate(friend_request.receiver_email, subject, params, 'invite.html', 'invite.txt')

def sendActivationLink(to_email, parameters):
    subject = "Verify your Email Id with Jobhunt.in"
    sendWithTemplate(to_email, subject, parameters, 'recruiterActivationLink.html', 'recruiterActivationLink.txt')

def sendPasswordResetLink(to_email, parameters):
    subject = "Jobhunt.in password reset."
    sendWithTemplate(to_email, subject, parameters, 'passwordChangeLink.html', 'passwordChangeLink.txt')

def sendMatchingProfiles(to_email, parameters):
    subject = parameters['subscription'][:75] + ' ....'
    sendWithDjangoTemplate(to_email, subject, parameters, 'matchingprofiles.html')

def sendUserReport(to_email, parameters):
    subject = 'Your profile was emailed to '+ parameters['num_of_sends'] +' recruiters'
    sendWithDjangoTemplate(to_email, subject, parameters, 'userreport.html')

def sendRecruiterInvites(to_email, parameters):
    subject = "Exclusive Recruiter Invite - Join Jobhunt.in for Free (via " + parameters['from'] + ")"
    sendWithDjangoTemplate(to_email, subject, parameters, 'recinvite.html')

def sendInterestedRecruitersList(to_email, parameters):
    subject = "Recruiters have requested for your resume"
    sendWithDjangoTemplate(to_email, subject, parameters, 'interested_recs.html')

def sendAnonUserWelcomeMail(to_email, parameters):
    subject = "Welcome to Jobhunt.in"
    sendWithTemplate(to_email, subject, parameters, 'anonuserwelcome.html', 'anonuserwelcome.txt')

def sendAdminRecruiterInvites(to_email, parameters, subject=None):
    if not subject: subject = "Exclusive Recruiter Invite - Join Jobhunt.in for Free"
    sendWithDjangoTemplate(to_email, subject, parameters, 'sprecinvite.html', '"Aravind" <aravind@jobhunt.in>')

def sendWithTemplate(to_email, subject, parameters, html_filename, txt_filename):
    sender='"Jobhunt.in" <mailman@jobhunt.in>'
    template_dir = '/apps/jobhuntin/backslash/mailtemplates/'
    html_filename = template_dir + html_filename
    txt_filename = template_dir + txt_filename
    template_html = open(html_filename, 'r').read()
    template_text = open(txt_filename, 'r').read()

    html_body = Template(template_html).safe_substitute(parameters)
    text_body = Template(template_text).safe_substitute(parameters)
    mailman.sendOneWayMail(sender, [to_email], subject, html_body, text_message=text_body)

def sendWithDjangoTemplate(to_email, subject, parameters, html_filename, sender=None):
    if not sender:    sender='"Jobhunt.in" <mailman@jobhunt.in>'
    template_dir = '/apps/jobhuntin/backslash/mailtemplates/'
    html_filename = template_dir + html_filename
    template_html = open(html_filename, 'r').read()

    html_body = django_templater.render(template_html, parameters)

    mailman.sendOneWayMail(sender, [to_email], subject, html_body)
