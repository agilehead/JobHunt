#!/usr/bin/env python
from __future__ import with_statement

import os, cPickle, datetime, string
import psycopg2, re, sys, shutil, time
sys.path.append('/apps/jobhuntin/backslash')
from subprocess import call
from utils import dataplus, eventnotifier, mailer

def sendRequests():
    new_time = str(datetime.datetime.utcnow())

    if os.path.exists(time_stamp_file):
        last_time_stamp = ''
        with open(time_stamp_file, 'r') as f:
            last_time_stamp = f.readline()
        if not last_time_stamp or last_time_stamp == '':
            last_time_stamp = str(datetime.datetime(1980, 10, 3))
        if last_time_stamp[-1] == '\n':
            last_time_stamp = last_time_stamp[:-1]
    else:
        last_time_stamp = str(datetime.datetime(1980, 10, 3))
        with open(time_stamp_file, 'w') as f:
            f.write(last_time_stamp + '\n')

    sendResumeRequestToUsers(last_time_stamp)

    with open(time_stamp_file, 'w') as f:
        f.write(new_time + '\n')

def sendResumeRequestToUsers(last_time_stamp):
    print last_time_stamp
    #get the data from PostgreSql
    stmt = """SELECT U.id, U.email FROM website_user U INNER JOIN website_account A ON U.account_id = A.id
                WHERE A.account_type = 'PU' AND A.account_state = 'A' AND U.id IN
                    (SELECT CAST("key" as integer) FROM website_notification WHERE type='ProfViewed' AND activity_time > %(last_time_stamp)s)"""
    cursor.execute(stmt, {'last_time_stamp':last_time_stamp})
    users_to_mail = cursor.fetchall()

    required_formats = ['html']
    for row in users_to_mail:
        try:
            print row[1], ' has to be mailed.'
            
            stmt = "SELECT text FROM website_notification WHERE key=%(user_id)s AND type='ProfViewed' ORDER BY activity_time DESC"
            cursor.execute(stmt, {'user_id':str(row[0])})
            req_list = cursor.fetchall()
            
            recs = getFilteredRecruiterList(req_list)
            mailer.sendInterestedRecruitersList(row[1], {'num_of_sends':str(len(recs)),
                                                        'recruiter_infos':recs,
                                                        'date':datetime.datetime.utcnow()})
        except:
            ex_type = sys.exc_info()[0]
            ex_msg = sys.exc_info()[1]
            print ex_type, ex_msg
            logError('Unknown error: Skipping user ' + row[1] + ': ' +  str(ex_type) +  str(ex_msg))
    
def getFilteredRecruiterList(result_rows):
    recs = []
    rec_ids = []
    for row in result_rows:
        dict = cPickle.loads(str(row[0]))
        if not dict['recruiter_id'] in rec_ids:    
            stmt = """SELECT R.id, R.name, R.email, R.organization, RS.keywords, RS.experience, RS.location, RS.job_title, RS.job_company, RS.job_description 
                FROM website_recruiter R INNER JOIN website_recruitersubscription RS ON RS.recruiter_id = R.id
                WHERE R.id = %(recruiter_id)s AND RS.id = %(subscription_id)s"""
            cursor.execute(stmt, dict)
            rec_id, name, email, organization, filter_keywords, filter_experience, \
                filter_location, job_title, job_company, job_description = cursor.fetchone()
            
            rec_info = {'name':name, 'email':email, 'organization':organization, 'filter_keywords':filter_keywords,
                        'filter_experience':filter_experience, 'filter_location':filter_location,
                        'job_title':job_title, 'job_company':job_company, 'job_description':job_description}
            
            recs.append(rec_info)
            rec_ids.append(rec_id)
            
    return recs

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/send_resume_request_job_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    eventnotifier.sendEventNotification("Jobhunt Job Error: send_resume_request_job", err)

conn_str = "dbname='jhindb' user='jhindbu' password='*password#' host='127.0.0.1'"
#workspace_path = '/skillda/system/temp/docshare'
time_stamp_file = '/apps/jobhuntin/backslash/jobs/send_resume_request_job_time_stamp.txt'

connection = psycopg2.connect(conn_str)
cursor = connection.cursor()

if __name__ == "__main__":
    sendRequests()
