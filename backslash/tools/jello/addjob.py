#!/usr/bin/env python

import sys
import getopt
import sqlite3 as sqlite

connstr = 'mailinglist.sqlite'

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hj:s:t:c:p:i:", ["help", "jobname", "subject", "template", "conditions", "params", "identifier"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    jobname = subject = template = identifier = None
    conditions = ''
    params = ''

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-j', '--jobname'):
            jobname = a
        if o in ('-s', '--subject'):
            subject = a        
        if o in ('-t', '--template'):
            template = a        
        if o in ('-c', '--conditions'):
            conditions = a
        if o in ('-p', '--params'):
            params = a
        if o in ('-i', '--identifier'):
            identifier = a
        
    if jobname and subject and template and identifier:
        try:
            connection = sqlite.connect(connstr)    
            cursor = connection.cursor()
            
            #the identifier itself is a param. add it to params
            if params == '':
                params = 'ji=' + identifier
            else:
                params += ';ji=' + identifier
            
            #check if the jobname already exists
            #if (cursor.execute('select * from jobs where name=:jobname', {'jobname':jobname}).fetchone() != None)
                       
            cursor.execute('insert into jobs (name, subject, template, conditions, params, identifier) values (?,?,?,?,?,?)', (jobname, subject, template, conditions, params, identifier))
            connection.commit()
            print('Job added.')
        except:
            print('Error.')
            connection.rollback()
    
    else:
        usage()
        sys.exit(2)
    
def usage():
    print('Usage:')
    print('addjob.py -j job_name -s subject -t template_path -c conditions -p params -i identifier')
    print('conditions can be:')
    print('     all')
    print('     tags=recruiter,jobseeker')
    print('params (which will be passed to a template) can be:')
    print('     reason=New Year;message=Happy New Year!')
    print('identifier is a unique name used to track campaing responses. This will be matched with values in web server log files.')
    print('Note that the identifier itself is used added as a param.')
    
if __name__ == "__main__":
    main()