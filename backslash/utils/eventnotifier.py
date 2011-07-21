#!/usr/bin/env python
import mailman

def sendEventNotification(subject, body=''):
    html_body = body.replace('\n','<br />')
    mailman.sendOneWayMail('"Jobhunt Admin" <admin@jobhunt.in>', ['notify@jobhunt.in'], subject, html_body, text_message=body)
    