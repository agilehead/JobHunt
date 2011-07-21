#!/usr/bin/env python
from __future__ import with_statement

import os, time, datetime, random, re, string, sys
import psycopg2, shutil

sys.path.append('/apps/jobhuntin/backslash')
from utils import config, dataplus, eventnotifier

sys.path.append('/apps/socialray/common/pylibs')
from search_client import SearchClient, IndexUpdateEntry, DataFormatter as format

CLUSTER_ID = 'backslash_resumes'
time_stamp_file = '/apps/jobhuntin/backslash/jobs/trinity_feed_job_time_stamp.txt'

#get the data from PostgreSql
connection = psycopg2.connect(config.conn_str)
cursor = connection.cursor()

def feedResumes(limit_time):
    s = SearchClient()
    
    #deleted users have to be moved from index
    stmt = "SELECT user_id FROM website_indexdelta WHERE index_type = 'D' AND marked_at < %(limit_time)s;"
    cursor.execute(stmt, {'limit_time':limit_time})
    results = cursor.fetchall()
    deletions = []
    for row in results:
        print 'deleting.. ', str(row[0])
        deletions.append(IndexUpdateEntry('delete', str(row[0])))
        
    s.updateIndexes(deletions, CLUSTER_ID)

    #indexing the updated users
    stmt = """SELECT U.id, A.account_type, A.username, U.key, (CASE A.account_type WHEN 'FU' THEN U.email WHEN 'PU' THEN U.proxy_email END) As email,
            name, telephone, industry, experience, curr_employer, curr_designation, tags, summary, min_salary, pref_employment,
            pref_designation, pref_location, text_filepath, rating
            FROM website_user U INNER JOIN website_account A ON U.account_id = A.id
            WHERE U.id IN (SELECT user_id FROM website_indexdelta WHERE index_type = 'U' AND marked_at < %(limit_time)s)
            AND A.account_state = 'A' AND U.is_job_hunting = 'yes' ORDER BY U.id;"""
    cursor.execute(stmt, {'limit_time':limit_time})
    results = cursor.fetchall()

    update_list = []
    for (user_id, account_type, username, key, email, name, telephone, industry, experience, curr_employer, curr_designation, \
        tags, summary, min_salary, pref_employment, pref_designation, pref_location, text_filepath, rating) in results:
        
        if account_type == 'PU' or (account_type == 'FU' and text_filepath and os.path.exists(text_filepath)):
            
            meta = {}
            meta['id'] = str(user_id)
            meta['account_type'] = dataplus.decode(account_type)
            meta['username'] = dataplus.decode(username)
            meta['name'] = dataplus.decode(name)
            meta['key'] = dataplus.decode(key)
            meta['email'] = dataplus.decode(email)
            meta['telephone'] = dataplus.decode(telephone)
            meta['industry'] = dataplus.decode(industry)
            meta['experience'] = format.Int(experience)
            meta['curr_employer'] = dataplus.decode(curr_employer)
            meta['curr_designation'] = dataplus.decode(curr_designation)
            meta['tags'] = dataplus.decode(tags)
            meta['summary'] = dataplus.decode(summary)
            meta['min_salary'] = format.Int(min_salary)
            meta['pref_employment'] = dataplus.decode(pref_employment)
            meta['pref_designation'] = dataplus.decode(pref_designation)
            meta['pref_location'] = dataplus.decode(pref_location)
            meta['rating'] = format.Int(rating)
            meta['indexed_on'] = format.Date(limit_time)

            if account_type == 'FU':
                meta['fulltext'] = format.exactFormat(meta['tags'] + dataplus.decode(open(text_filepath).read()))
            elif account_type == 'PU':
                meta['fulltext'] = format.exactFormat(meta['tags'] + '\n' + meta['summary'])
                
            update_list.append(IndexUpdateEntry('update', str(user_id), meta))
            print user_id, dataplus.decode(meta['tags'])

    print 'finished creating meta data'
    #we are updating the Resume Store (store-name:resume)
    s.updateIndexes(update_list, CLUSTER_ID)
    print "updated indexes successfully"

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/trinity_feed_job_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    print "Stopping job:", err
    eventnotifier.sendEventNotification("Jobhunt Job Error: trinity_feed_job", err)

if __name__ == "__main__":
    time_now = datetime.datetime.utcnow()
    print time_now
    
    try:
        #process starts here....
        feedResumes(time_now)
    
        #clearing the index delta
        stmt = "DELETE FROM website_indexdelta WHERE marked_at < %(time_now)s;"
        cursor.execute(stmt, {'time_now': time_now})
        connection.commit()
    except:
        logError('Feeding index updates to solr failed : ' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))
        