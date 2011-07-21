#!/usr/bin/env python

import sys
import getopt
import sqlite3 as sqlite

connstr = 'mailinglist.sqlite'

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hj:d", ["help","jobname","destroy"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    jobname = None
    destroy = False

    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-j', '--jobname'):
            jobname = a
        if o in ('-d', '--destroy'):
            destroy = True
        
    if jobname:
        try:
            connection = sqlite.connect(connstr)    
            cursor = connection.cursor()
            
            if not destroy:
                cursor.execute('update jobs set deleted=1 where name=:jobname', {'jobname':jobname})
            else:
                cursor.execute('delete from jobs where name=:jobname', {'jobname':jobname})
                
            connection.commit()
            
            print('Job deleted.')
        except:
            print(sys.exc_info())
            print('Error.')
            connection.rollback()
    
    else:
        usage()
        sys.exit(2)
    
def usage():
    print('Usage:')
    print('python removejob -j jobname [-d]')
    print('The -d option deletes the job from the database, making it unavailable for reporting later. Use carefully.')
    
if __name__ == "__main__":
    main()