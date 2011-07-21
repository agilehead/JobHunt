#!/usr/bin/env python
from __future__ import with_statement

import datetime, os, psycopg2, re, sys, string
sys.path.append('/apps/jobhuntin/backslash')
from utils import mailer, eventnotifier, notifications, search_helper

default_min_datetime = datetime.datetime(1980, 10, 3)
job_start_time = datetime.datetime.utcnow()

class TempSubscription:
    pass

#recruiter_id, R.key, email, RS.id, keywords, experience, RS."location", industry, max_salary, min_count, results_last_sent_on
def getSubscriptionFromRow(row):
    subscr = TempSubscription()
    subscr.recruiter_id = row[0]
    subscr.recruiter_key = row[1]
    subscr.recruiter_email = row[2]
    subscr.id = row[3]
    subscr.keywords = row[4]
    subscr.experience = row[5]
    subscr.location = row[6]
    subscr.industry = row[7]
    subscr.max_salary = row[8]
    subscr.min_count = row[9]
    subscr.results_last_sent_on = row[10]

    return subscr
    
def mailMatchingUsers():
    #get the data from PostgreSql
    stmt = """SELECT recruiter_id, R.key, email, RS.id, keywords, experience, RS."location", industry, max_salary, min_count, results_last_sent_on
            FROM website_recruitersubscription AS RS INNER JOIN website_recruiter AS R ON RS.recruiter_id = R.id
            INNER JOIN website_account AS A ON R.account_id = A.id
            WHERE keywords <> '' AND A.account_state = 'A' AND A.email_verified = TRUE AND R.verified = TRUE"""
    cursor.execute(stmt)
    results = cursor.fetchall()

    for row in results:
        subscription = getSubscriptionFromRow(row)
        sendSubscriptionResults(subscription, subscription.recruiter_id, subscription.recruiter_key, subscription.recruiter_email, True)
    connection.commit()

def sendSubscriptionResults(subscription, rec_id, rec_key, rec_email, from_job=False):
    #try:
        print rec_email

        response = search_helper.matchResumes(subscription.keywords, subscription.experience, subscription.location, subscription.max_salary, subscription.results_last_sent_on)
        if string.atoi(response.numFound) >= subscription.min_count:
            sendMailToRecruiter(response.results, subscription, rec_email, rec_key)
            logSentUsers(response.results, rec_email, subscription.id)
        if not from_job:    connection.commit()
    #except:
    #    logError('Failed sending matches to recruiter: %d(%s) with error: %s, %s' % (subscription.id, rec_email, str(sys.exc_info()[0]), str(sys.exc_info()[1])))

def logSentUsers(users, rec_email, subscription_id):
    user_ids = [user['id'] for user in users]
    for user_id in user_ids:
        notifications.addNotification(user_id, 'ProfEmailed', data={'recruiter_email':rec_email, 'subscription_id':subscription_id})
    notifications.addNotification(rec_email, 'SubResults', ','.join(map(str, user_ids)))
    stmt = 'UPDATE website_recruitersubscription SET results_last_sent_on = %(job_start_time)s;'
    cursor.execute(stmt, {'job_start_time':job_start_time})

def createMailContext(matches, subscription, recruiter_key):
    context = {}
    context['subscription_id'] = subscription.id
    subscription_text = subscription.keywords
    if subscription.experience:  subscription_text += ' with %d years' % subscription.experience
    if not subscription.location.lower() == 'any':    subscription_text += ' in ' + subscription.location
    context['subscription'] = subscription_text
    context['date'] = datetime.datetime.utcnow().strftime('%B %e, %Y')

    user_list = []
    for usr in matches[:10]:
        min_salary_desc = ''
        if usr['min_salary']:    usr['min_salary'] = '%d Lakhs' % (usr['min_salary']/100000)
        #Software Engineer with Helzinger Consulting, 7 years exp, in Bangalore.
        usr['profile_info'] = ('Fresher', "%s with %s, %d years of experience." % (usr['curr_designation'], usr['curr_employer'], usr['experience']))[usr['experience'] > 0]

        summary_html = ''
        if usr['summary']:
            summary_html =  string.join([x.strip() for x in re.split('\n+', re.sub('\r?\n', '\n', usr['summary'])) if re.match('[a-zA-Z]{2,}', x.strip())], ' <strong> | </strong> ') + '.'
            if len(summary_html) > 300: summary_html = summary_html[:297] +'...'
            if summary_html.rfind('<strong>') > summary_html.rfind('</strong>'):   summary_html = summary_html[:summary_html.rfind('<strong>')].strip() + '...'
            usr['summary'] = summary_html
        usr['is_premium_user'] = (usr['account_type'] == 'PU')
        user_list.append(usr)

    #print 'matching users:', len(user_list)
    context['matching_users'] = user_list
    context['num_results'] = len(matches)
    return context

def sendMailToRecruiter(matching_users, subscription, recruiter_email, recruiter_key):
    context = createMailContext(matching_users, subscription, recruiter_key)
    mailer.sendMatchingProfiles(recruiter_email, context)

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/recruiter_mail_job_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    eventnotifier.sendEventNotification("Jobhunt Job Error: recruiter_mail_job", err)


conn_str = "dbname='jhindb' user='jhindbu' password='*password#' host='127.0.0.1'"
#time_stamp_file = '/apps/jobhuntin/backslash/jobs/recruiter_mail_job_time_stamp.txt'
connection = psycopg2.connect(conn_str)
cursor = connection.cursor()

if __name__ == "__main__":
    mailMatchingUsers()
