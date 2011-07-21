#!/usr/bin/env python

from __future__ import with_statement 
import sys
import getopt
import sqlite3 as sqlite

connstr = 'mailinglist.sqlite'

def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:t:", ["help","filename","tags"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    filename = None
    tags = ''
    
    for o,a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-f', '--filename'):
            filename = a
        if o in ('-t', '--tags'):
            tags = a        
        
    if filename:
        try:
            connection = sqlite.connect(connstr)    
            cursor = connection.cursor()            
            
            with open(filename, "r") as f:
                added_emails = []
                for line in f.xreadlines():
                    email,params_entry = line.split(';')
                    
                    
                    #often, emails occur multiple times in the same list.
                    #ignore the second.
                    if email in added_emails:
                        continue
                    else:
                        added_emails.append(email)
                    
                    #see if the record already exists.
                    #if so, do not create a new entry. simply add new tags.
                    existing_record = cursor.execute('select tags from mailinglist where email=:email', {'email': email}).fetchone()
                    if (existing_record and len(existing_record) > 0):
                        old_tag = existing_record[0]
                        if (old_tag):
                            combined_tags = old_tag + ',' + tags
                        else:
                            combined_tags = tags
                        cursor.execute('update mailinglist set tags=:tags where email=:email', {'tags': combined_tags, 'email': email})
                    else:
                        cursor.execute('insert into mailinglist (email, tags, params) values (?,?,?)', (email.rstrip(), tags, params_entry))
            
            print('The mail addresses were added to the database.')
            connection.commit()
        except:
            print('Error.')
            print(sys.exc_info())
            connection.rollback()
    
    else:
        usage()
        sys.exit(2)
    
def usage():
    print('Usage:')
    print('addtomailinglist.py -f filename -t tags')
    
if __name__ == "__main__":
    main()