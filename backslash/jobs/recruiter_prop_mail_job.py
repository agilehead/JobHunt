from __future__ import with_statement
from django.http import HttpResponse, HttpResponseRedirect

import datetime, os, psycopg2, re, sys, string
sys.path.append('/apps/jobhuntin/backslash')
from utils import dataplus, mailer, notifications, search_helper
from website import models, codejar

#R.id, key, name, organization, email
class RecInfo(object):
    def __init__(self, row):
        self.id = row[0]
        self.key = row[1]
        self.name = row[2]
        self.organization = row[3]
        self.email = row[4]
        self.token_value = row[5]
        
def mailUsers():
    #get the data from PostgreSql
    stmt = """SELECT R.id, key, name, organization, email, T.value AS token_value
        FROM website_recruiter AS R INNER JOIN website_token AS T ON T.owner = R.email
        INNER JOIN website_account AS A ON R.account_id = A.id WHERE A.account_state = 'I' AND A.email_verified = TRUE"""
    cursor.execute(stmt)
    results = cursor.fetchall()

    min_datetime = datetime.datetime(1980, 10, 3)   #min_date
    mailing_list = getMailingList()
    for row in results:
        rec = RecInfo(row)
        
        for (subject, usr_list) in mailing_list:
            print('sending email to ' + rec.email + 'invite link http://jobhunt.in/recruiters/dashboard.htm?rec_token=' + rec.token_value)
            mailer.sendAdminRecruiterInvites(rec.email, {'token':rec.token_value, 'key':rec.key, 'matching_users':usr_list, 'header':subject}, subject)
            for usr in usr_list:
                notifications.addNotification(usr['id'], 'ProfEmailed', data={'recruiter_id':rec.id, 'recruiter_email':rec.email})
            notifications.addNotification(rec.email, 'PropResults', ','.join([str(usr['id']) for usr in usr_list]))

def addFormatting(users):
    for usr in users:
        min_salary_desc = ''
        if usr['min_salary']:    usr['min_salary'] = '%d Lakhs' % (usr['min_salary']/100000)
        #Software Engineer with Helzinger Consulting, 7 years exp, in Bangalore.
        usr['profile_info'] = ('Fresher', "%s with %s, %d years of experience." % (usr['curr_designation'], usr['curr_employer'], usr['experience']))[usr['experience'] > 0]

        if usr['summary']:
            summary_html =  string.join([x.strip() for x in re.split('\n+', re.sub('\r?\n', '\n', usr['summary'])) if re.match('[a-zA-Z]{2,}', x.strip())], ' <strong> | </strong> ') + '.'
            if len(summary_html) > 300: summary_html = summary_html[:297] +'...'
            if summary_html.rfind('<strong>') > summary_html.rfind('</strong>'):   summary_html = summary_html[:summary_html.rfind('<strong>')].strip() + '...'
            usr['summary'] = summary_html
        usr['is_premium_user'] = (usr['account_type'] == 'PU')

    return users
        
def getUserFromRow(row):
    (id, key, email, name, industry, experience, curr_employer, curr_designation, tags, summary, min_salary,
     pref_employment, pref_designation, pref_location, account_type) = row
    
    user_info = {'id':id, 'key':key, 'email':email, 'name':name, 'industry':industry, 'experience':experience, 'curr_employer':curr_employer,
                 'curr_designation':curr_designation, 'tags':tags, 'summary':summary, 'min_salary':min_salary, 'pref_employment':pref_employment,
                 'pref_designation':pref_designation, 'pref_location':pref_location, 'account_type':account_type}
    return user_info

def getMailingList():
    new_list = []
    with open(selected_users_file) as f:
        for line in f.readlines():
            (subject, users_str) = line.strip().split('|')
            
            stmt = """SELECT U.id, U.key, (CASE A.account_type WHEN 'FU' THEN U.email WHEN 'PU' THEN U.proxy_email END) As email,
                    U.name, U.industry, U.experience, U.curr_employer, U.curr_designation, U.tags, U.summary, U.min_salary,
                    U.pref_employment, U.pref_designation, U.pref_location, A.account_type
                    FROM website_user AS U INNER JOIN website_account AS A ON U.account_id = A.id WHERE U.id IN (%s)
                    ORDER BY U.id DESC;""" % (users_str)
            cursor.execute(stmt)
            users = []
            for row in cursor.fetchall():
                users.append(getUserFromRow(row))
            new_list.append((subject, addFormatting(users)))
            
    return new_list


conn_str = "dbname='jhindb' user='jhindbu' password='*password#' host='127.0.0.1'"
#time_stamp_file = '/apps/jobhuntin/backslash/jobs/recruiter_mail_job_time_stamp.txt'
selected_users_file = '/apps/jobhuntin/backslash/jobs/recruiter_prop_user_list.txt'
connection = psycopg2.connect(conn_str)
cursor = connection.cursor()

if __name__ == "__main__":
    mailUsers()
