#!/usr/bin/env python
from __future__ import with_statement

import datetime, os, psycopg2, re, sys, string
sys.path.append('/apps/jobhuntin/backslash')
from utils import mailer, eventnotifier, config, notifications

default_min_datetime = datetime.datetime(1980, 10, 3)

class RecruiterInfo:
    def __init__(self, row_result, notification_id):
        self.name = row_result[0]
        self.organization = row_result[1]
        self.email = row_result[2]
        if len(row_result) > 3:
            self.subscription_keywords = row_result[3]
            self.subscription_experience = row_result[4]
            self.subscription_location = row_result[5]
            self.job_title = row_result[6]
            self.job_company = row_result[7]
            self.job_description = row_result[8]
        self.notification_id = notification_id

class UserInfo:
    def __init__(self, row_result):
        self.id = row_result[0]
        self.name = row_result[1]
        self.email = row_result[2]

def startSendingMail():
    print 'Starting to send report emails to users....'
    user_infos = getUsersToSendReports()
    if user_infos:
        recruiters_info = {}
        for user_info in user_infos:
            recruiter_notification_infos = getMailedRecruitersInfo(user_info.id)
            if recruiter_notification_infos:
                sendMailToUser(user_info, recruiter_notification_infos)
    print 'Done sending emails, bye!'

def sendMailToUser(user_info, recruiter_notification_infos):
    context = createMailContext(user_info, recruiter_notification_infos)
    mailer.sendUserReport(user_info.email, context)
    print 'email sent to ' + user_info.email
    logSentReport(user_info.id, context)
    clearRecruiterNotificationLog(recruiter_notification_infos)
    connection.commit()

def clearRecruiterNotificationLog(notification_infos):
    ids = ''
    for info in notification_infos:
        ids += str(info.notification_id) + ','
    stmt = """DELETE FROM WEBSITE_NOTIFICATION WHERE ID IN (%s);""" % ids.strip(',')
    cursor.execute(stmt)

def createMailContext(user_info, recruiter_notification_infos):
    context = {}
    context['user_name'] = user_info.name

    recruiter_infos = []
    for rec_info in recruiter_notification_infos:
        recruiter_info = {'name':rec_info.name, 'organization':rec_info.organization, 'email':rec_info.email,
                          'filter_keywords':rec_info.subscription_keywords, 'filter_experience':rec_info.subscription_experience,
                          'filter_location':rec_info.subscription_location, 'job_title': rec_info.job_title,
                          'job_company': rec_info.job_company,
                          'job_description': rec_info.job_description}
        recruiter_infos.append(recruiter_info)
        
    context['num_of_sends'] = str(len(recruiter_infos))
    context['recruiter_infos'] = recruiter_infos
    context['date'] = datetime.datetime.utcnow()
    return context

def getUsersToSendReports():
    stmt = """SELECT DISTINCT U.ID, U.NAME, U.EMAIL FROM
                WEBSITE_NOTIFICATION AS N,
                WEBSITE_USER AS U
                WHERE
                N.TYPE = 'ProfEmailed' AND 
                CAST(N.KEY AS INTEGER) = U.ID"""
    cursor.execute(stmt)
    results = cursor.fetchall()

    user_infos = ''
    if results:
        user_infos = [UserInfo(row) for row in results]        
    else:
        print 'No emails to be sent to the recruiters for any of the users'
        
    return user_infos

def getMailedRecruitersInfo(user_id):
    notifys = notifications.getNotificationTexts(str(user_id), 'ProfEmailed')

    #DISTINCT - Incase there were multiple updates on the resume and the resume was sent to the recruiter more than once
    stmt1 = """SELECT DISTINCT ON (R.ID, RS.ID)
                R.NAME, R.ORGANIZATION, R.EMAIL, RS.KEYWORDS, RS.EXPERIENCE, RS.LOCATION,
                RS.JOB_TITLE, RS.JOB_COMPANY, RS.JOB_DESCRIPTION FROM
                WEBSITE_RECRUITER AS R, WEBSITE_RECRUITERSUBSCRIPTION AS RS
                WHERE
                R.email = %(recruiter_email)s AND
                RS.ID = %(subscription_id)s AND
                RS. RECRUITER_ID = R.ID"""
    
    stmt2 = """SELECT NAME, ORGANIZATION, EMAIL FROM WEBSITE_RECRUITER WHERE EMAIL = %(recruiter_email)s"""
    recruiter_notification_infos = []

    #format of notification - 'notification_id':row[0],'text':cPickle.loads(row[1])
    #format of notification text - 'recruiter_email':rec_email, 'subscription_id':subscription_id
    for notification in notifys:
        rec_email = notification['text']['recruiter_email']
        if notification['text'].has_key('subscription_id'):
            subscr_id = notification['text']['subscription_id']
            cursor.execute(stmt1, {'recruiter_email':rec_email, 'subscription_id':subscr_id})
        else:
            cursor.execute(stmt2, {'recruiter_email':rec_email})
            
        results = cursor.fetchall()
        if results:
            for row in results:
                recruiter_notification_infos.append(RecruiterInfo(row, notification['notification_id']))

    return recruiter_notification_infos

def logSentReport(user_id, context):
    notifications.addNotification(user_id, 'UserReport', data=context)

conn_str = config.conn_str
time_stamp_file = '/apps/jobhuntin/backslash/jobs/recruiter_mail_job_time_stamp.txt'
connection = psycopg2.connect(conn_str)
cursor = connection.cursor()

if __name__ == "__main__":
    startSendingMail()
