#!/usr/bin/env python
from __future__ import with_statement
import sys
import getopt
import sqlite3 as sqlite

connstr = 'mailinglist.sqlite'

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:l:i:", ["help","updatename", "logfile","identifier"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    updatename = identifier = None
    logfile = 'access.log'
    
    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-u', '--updatename'):
            updatename = a
        if o in ('-l', '--logfile'):
            logfile = a
        if o in ('-i', '--identifier'):
            identifier = a
    
    if updatename and identifier:    
        try:
            connection = sqlite.connect(connstr)
            cursor = connection.cursor()
            
            with open(logfile) as log:
                 for line in log.xreadlines():
                    for a in line.split('\t'):
                        print a
        
            print ('Printed.')

        except:
            print(sys.exc_info())
            print('Error.')
            connection.rollback()
    
    else:
        usage()
        sys.exit(2)
        
    
def usage():
    print('Usage:')
    print('python parselogs -u updatename -l logfilename -i identifier')
    print(' updatename is a name give to the log file import job. It is used if we need to rollback.')
    print(' identifier is the value of the param in the GET HTTP request.')
    
if __name__ == "__main__":
    main()