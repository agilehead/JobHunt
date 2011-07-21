from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

import string,datetime
from website import models, codejar
from utils import dataplus, i18n, mailman, mailer, eventnotifier

def handle(request):    
    if request.method == 'GET':         
        return codejar.actions.render(request, 'tellfriends.htm')
        
    elif request.method == 'POST':
        sender_name = dataplus.dictGetSafeVal(request.REQUEST, 'name')
        emails = []
        emails[len(emails):] = dataplus.dictGetSafeVal(request.REQUEST, 'email1', '').split(',')
        emails[len(emails):] = dataplus.dictGetSafeVal(request.REQUEST, 'email2', '').split(',')
        emails[len(emails):] = dataplus.dictGetSafeVal(request.REQUEST, 'email3', '').split(',')
        message = dataplus.dictGetSafeVal(request.REQUEST, 'messageBox')
        
        valid_emails = [eml for eml in emails if eml != '']
        if sender_name and valid_emails and message:
            ip_address = request.META['REMOTE_ADDR']
            sent_count = getSentRequestCount(ip_address)
            send_max = 6 - sent_count
            if send_max < 0:    send_max = 0
            
            requests = []
            for email_id in valid_emails:
                fr = models.TellFriend(sender_name=sender_name, 
                                        receiver_email=email_id, 
                                        message=message,
                                        ip_address=ip_address)
                fr.save()
                requests.append(fr)
            
            subject = 'New Tell Friends Request'
            if send_max < len(valid_emails):    subject += ": Require verification"
            event_desc = "Sender: %s\nReceiver(s): %s\nMessage: %s" % (sender_name, string.join(valid_emails, ','), message)
            eventnotifier.sendEventNotification(subject, event_desc)
            
            for req in requests[:send_max]:
                mailer.sendInviteFriend(req)
                req.sent = True
                req.save()
            
            return HttpResponseRedirect('toldfriends.html')
        else:
            return HttpResponse('Gimme some valid data :(')

def getSentRequestCount(ip_address):
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day)
    return models.TellFriend.objects.filter(ip_address=ip_address, requested_at__gte=today).count()
