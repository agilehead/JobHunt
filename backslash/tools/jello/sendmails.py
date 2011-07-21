#!/usr/bin/env python

from __future__ import with_statement 
import sys
import getopt
import sqlite3 as sqlite
import string
import psycopg2
import mailer

connstr = 'ah-marketing.sqlite'
connection = sqlite.connect(connstr)
            
def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hj:s:", ["help","jobname","startid"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    jobname = None
    startid = 0
    
    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-j', '--jobname'):
            jobname = a
        if o in ('-s', '--startid'):
            startid = string.atoi(a)
        
    if jobname:
        try:
            cursor = connection.cursor()

            subject, template, conditions, job_params = cursor.execute('select subject, template, conditions, params from jobs where name=:jobname', {'jobname':jobname}).fetchone()
            
            #Currently only the 'tags' condition is supported.
            #This will send mails to everybody in the mailinglist, who has those tags.
            conditions = getDictionary(conditions)
            
            mailinglist = cursor.execute('select id, firstname, lastname, domain, tags, params from emailinfo where id >= :startid', {'startid': startid}).fetchall()
            for id, firstname, lastname, domain, receiver_tags, receiver_params in mailinglist:                
                #check for the tags condition
                #Logic: if target has all required tags, then send.
                
                if receiver_tags: all_tags = set(receiver_tags.split(','))
                else: all_tags = set({})
                
                if 'unsubscribed' in all_tags:  continue
                
                if conditions['tags']: required_tags = set(conditions['tags'].split(','))
                else: required_tags = set({})
                
                if (required_tags.issubset(all_tags)):
                    sendMail(id, email, subject, template, receiver_params, job_params, jobname)
                
        except:
            print sys.exc_info()
            print('Error.')
    
    else:
        usage()
        sys.exit(2)


def sendMail(id, email, subject, template, receiver_params, job_params, jobname):
    
    print ('Sending to ' + email)
    
    params = { 'jobname': jobname }
    params.update(getDictionary(receiver_params))
    params.update(getDictionary(job_params))
    
    mailer.sendWithTemplate(email, subject, params, template + '.html', template + '.txt')
    
    try:
        cursor = connection.cursor()
        cursor.execute('insert into emailtrylist (email, emailinfo, success) values (?,?,?)', (email, id, 1))
        cursor.execute('insert into outbox (jobname, email, receiver_params) values (?,?,?)', (jobname, email, receiver_params))
        connection.commit()        
    except:
        connection.rollback()


#format is key1=value1;key2=value2;...
def getDictionary(data, seperator=';'):
    dic = {}
    if data:
        items = data.split(seperator)
        for i in items:
            if '=' in i:
                key, val = i.split('=')                
                dic[key] = val
            else:
                dic[i] = None
    return dic

def usage():
    print('Usage:')
    print('sendmails.py -j jobname [-s id_to_start_from]')


#need to access utils module
#sys.path += ['../../utils']
#import mailer
if __name__ == "__main__":
    main()