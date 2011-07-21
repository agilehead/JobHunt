#!/usr/bin/env python
from __future__ import with_statement

import datetime, os, string
import smtplib

log_folder_path = '/apps/jobhuntin/backslash/logs/smtprelay'

def sendLocal(sender, recipients, msg):
    msg['From'] = '"Jobhunt.in" <mailman@jobhunt.in>'
    smtp = smtplib.SMTP()
    smtp.connect('localhost', 25)
    smtp.sendmail(sender, recipients, msg.toMIMEMultipart().as_string())
    smtp.quit()

def sendMail(sender, recipients, msg):
    if recipients == ['notify@jobhunt.in']:
        #no need to relay
        sendLocal(sender, recipients, msg)
    else:
        relay_data = getRelayDetails()
        if relay_data:
            
            #replace the sender, since we are relaying.
            #that is, don't claim to be someone else.    
            #sender = '"Jobhunt.in" <' + relay_data[0] + '>'
            
            #msg['From'] = sender
            #msg['Sender'] = sender
            #msg['Reply-To'] = sender
            
            relay_server = 'smtpout.secureserver.net'
            smtp = smtplib.SMTP()
            smtp.connect(relay_server)
            smtp.login(relay_data[0], relay_data[1])
            smtp.sendmail(sender, recipients, msg.toMIMEMultipart().as_string())
            smtp.quit()
            logMail(sender, recipients, msg['Subject'])
        else:
            sendLocal(sender, recipients, msg)
        
        
    #We have to fix the from address.
    #leave reply to as it is.    
def getRelayDetails():
    #we can send 220 mails a day through 1 email id.
    #host = 'smtpout.secureserver.net'

    logins = [('mailmana@job-huntin.com','*password#'),
        ('mailmanb@job-huntin.com','*password#'),
        ('mailmanc@job-huntin.com','*password#'),
        ('mailmand@job-huntin.com','*password#'),
        ('mailmane@job-huntin.com','*password#'),
        ('mailmanf@job-huntin.com','*password#'),
        ('mailmang@job-huntin.com','*password#'),
        ('mailmanh@job-huntin.com','*password#')]


    filepath = log_folder_path + '/' + datetime.datetime.utcnow().strftime('%Y%m%d')

    total_mails = 0
        
    if os.path.exists(filepath):
        with open(filepath) as f:
            line = f.readline()
            total_mails = string.atoi(line)
    
    index = total_mails/220

    if (index >= len(logins)):   return None
    
    with open(filepath, 'w') as f:
        f.write(str(total_mails + 1))
    
    return logins[index]

def logMail(sender, recipients, subject):
    try:
        f = open('/apps/jobhuntin/backslash/logs/mailman.log','w')
        f.write('Sender:' + sender + '; Recipient(s): ' + str(recipients) + '; Subject:' + subject + ', Time:' + str(datetime.datetime.utcnow()) + '\n')
    except:
        pass
    finally:
        if f:   f.close()
        