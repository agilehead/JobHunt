#!/usr/bin/env python
from __future__ import with_statement

import os, datetime, string
import psycopg2, re, sys, shutil, time
sys.path.append('/apps/jobhuntin/backslash')
from subprocess import call
from utils import dataplus, docserve_client, html2text, eventnotifier, mailer

def convert():
    new_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=30)
    date_format = "%Y-%m-%d %H:%M:%S"

    last_time_stamp = datetime.datetime(1980, 10, 3)
    if os.path.exists(time_stamp_file):
        with open(time_stamp_file, 'r') as f:
            try:
                last_time_stamp = datetime.datetime.strptime(f.readline().strip(), date_format)
            except:
                pass
    else:
        last_time_stamp = datetime.datetime(1980, 10, 3)
        with open(time_stamp_file, 'w') as f:
            f.write(last_time_stamp + '\n')

    convertResumes(last_time_stamp)

    with open(time_stamp_file, 'w') as f:
        f.write(new_time.strftime(date_format) + '\n')

def convertResumes(last_time_stamp):
    print last_time_stamp
    #get the data from PostgreSql
    connection = psycopg2.connect(conn_str)
    cursor = connection.cursor()
    stmt = """SELECT U.id, doc_filepath, key, mail_ref_id, U.email, U.summary, U.settings_edited, A.account_type FROM website_user U INNER JOIN website_account A ON U.account_id = A.id
                WHERE resume_updated_on > %(last_time_stamp)s ORDER BY id"""
    cursor.execute(stmt, {'last_time_stamp':last_time_stamp})
    results = cursor.fetchall()

    required_formats = ['html', 'txt']
    for row in results:
        try:
            print str(row[1]), 'needs doc conversion.'

            filename = row[1][row[1].rfind('/')+1:]
            #shutil.copy(row[1], workspace_path + '/' + filename)
            call(['cp %s %s/%s' %(row[1], workspace_path, filename)], shell=True)
            files = docserve_client.command('convert_file', filename + ',' + string.join(required_formats, ','))
            if files.startswith('error:'):
                logError('Error: Skipping resume : id #' + str(row[0]) + '. File conversion failed. ' + files[6:])
                continue

            resume_dir = '/'.join(row[1].split('/')[:-1])
            
            for file_info in files.split(','):
                new_filename = file_info.split('~')[1]
                new_filepath = resume_dir + '/' + new_filename
                
                call(['cp %s/%s %s' %(workspace_path, new_filename, new_filepath)], shell=True)
                #some cleanup
                try:
                    call(['rm -f %s/%s' %(workspace_path, new_filename)], shell=True)
                    call(['rm -f %s/%s' %(workspace_path, filename)], shell=True)
                    call(['rm -f -R %s/%s_files' %(workspace_path, filename[:filename.rfind('.')])], shell=True)
                except:
                    pass
            
            html_filepath = resume_dir + '/' + filename[:filename.rfind('.')] + '.html'
            text_filepath = resume_dir + '/' + filename[:filename.rfind('.')] + '.txt'
            text_content = ''
            with open(text_filepath) as text_file:
                text_content = text_file.read()            

            #Cleaning up unicode and converting to Ascii
            text_content = dataplus.toAscii(text_content)

            extracted_summary = row[5]  #summary
            if not row[6]:  #settings_edited
                try:
                    extracted_summary = parseSummary(text_content)
                except:
                    pass

            extracted_email = row[4]    #email
            if not extracted_email:
                #Email extraction...
                try:
                    extracted_email = parseEmail(text_content)
                    if extracted_email and row[7] == 'FU':  #account_type
                        verifyAndSendMail(extracted_email, row[0], row[2], (row[3] > 0), cursor)
                except:
                    print 'Error extracting email:', str(sys.exc_info())

            stmt = "UPDATE website_user SET html_filepath = %(html_filepath)s, text_filepath = %(text_filepath)s, summary = %(summary)s, email = %(email)s WHERE id = %(user_id)s;"
            cursor.execute(stmt, {'html_filepath':html_filepath, 'text_filepath':text_filepath, 'summary':extracted_summary, 'email':extracted_email, 'user_id':row[0]})

            print 'Finished processing file'
            #break ---To be removed
        except:
            ex_type = sys.exc_info()[0]
            ex_msg = sys.exc_info()[1]
            logError('Unknown error: Skipping resume. ' +  str(ex_type) +  str(ex_msg))

    connection.commit()

def verifyAndSendMail(user_email, user_id, user_key, by_mail, cursor):
    stmt = "SELECT U.id, A.id, A.account_type FROM website_user U INNER JOIN website_account A ON U.account_id = A.id WHERE A.account_state = 'A' AND U.email = %(user_email)s AND U.id <> %(user_id)s;"
    cursor.execute(stmt, {'user_email':user_email, 'user_id':user_id})
    results = cursor.fetchall()
    params = {'user_key': user_key }
    if results:
        ids = []
        for row in results:
            ids.append((row[0], row[1]))
            if row[2] == 'PU':
                mailer.sendPremiumUserLoginToUpdateAlert(user_email, by_mail = by_mail)
                return

        stmt = "UPDATE website_account SET account_state = 'I' WHERE id IN (" + string.join([str(x[1]) for x in ids], ',') + ");"
        cursor.execute(stmt)

        for idx in ids:
            cursor.execute("INSERT INTO website_indexdelta (user_id, index_type, marked_at) VALUES (%(user_id)s, 'D', CURRENT_TIMESTAMP);", {'user_id':idx[0]})

        mailer.sendResumeUpdatedMail(user_email, params)
    else:
        mailer.sendResumeAddedMail(user_email, params)

def cleanLine(text):
    clean_text = re.sub('^\s*[\(\[]?[a-zA-Z0-9\-\*][\)\]\.]?\s+(.*)', r'\1', text).strip().capitalize()
    if re.findall('[,\.;]', clean_text[-1]): clean_text = clean_text[:-1]
    return clean_text

def parseSummary(content):
    getHeaderText = lambda mat: [x for x in mat.groups() if x][0]
    clean_content = re.sub('_*\*{2}_*','', content)
    lines = re.split('\n+', clean_content)
    summary_dict = {}
    ctr = 0
    while ctr < len(lines):
        #print ctr, lines[ctr]
        header_match = re.match('^.*((Summary)|(Profile)|(Objective)|(Experience)|(Cerfication)|(Qualification)|(Education)|(Academic)).*', lines[ctr], re.IGNORECASE)
        if len(lines[ctr].split()) <= 5 and header_match:
            sub_list = []
            #print lines[ctr]
            sub_ctr = 1
            while ctr+sub_ctr < len(lines):
                if re.match('^.*?\w{5,}.*$', lines[ctr+sub_ctr]):
                    if len(lines[ctr+sub_ctr].split()) < 5: break
                    sub_list.append(cleanLine(lines[ctr+sub_ctr]))
                    #print lines[ctr+sub_ctr]
                sub_ctr += 1
            if sub_list:    summary_dict[getHeaderText(header_match)] = sub_list
            ctr += sub_ctr - 1
        elif re.match('^.*?certified.*$',lines[ctr],re.IGNORECASE):
            if not summary_dict.has_key('Certified'):   summary_dict['Certified'] = []
            summary_dict['Certified'].append(cleanLine(lines[ctr]))
            #summary_lines.append(re.findall('^.*?([a-z]+.*)$', lines[ctr], re.IGNORECASE)[0])
        ctr += 1

    if not summary_dict:
        if len(clean_content) > 2000:   lines = re.split('\r?\n', clean_content[:2000])
        if not summary_dict.has_key('Raw'):   summary_dict['Raw'] = []

        ctr = 0
        while ctr < len(lines) and len(summary_dict['Raw']) < 3:
            if len(lines[ctr].split()) > 5:
                summary_dict['Raw'].append(cleanLine(lines[ctr]))
            ctr += 1

##    for key,list in summary_dict.iteritems():
##        print key
##        for l in list: print '\t',l
    summary_lines = []
    header_sequence = ['Summary', 'Profile', 'Experience', 'Cerfication', 'Certified',
                        'Qualification', 'Education', 'Academic', 'Raw']#, 'Objective'
    for hdr_item in header_sequence:
        if len(summary_lines) > 4:  break
        if summary_dict.has_key(hdr_item):
            if hdr_item in ['Summary','Profile']:
                summary_lines = summary_dict[hdr_item]
                break
            #print hdr_item
            summary_lines.extend(summary_dict[hdr_item][:2])

    return string.join(summary_lines, '\n')

def parseEmail(content):
    re_email = re.compile('[a-z0-9]+[\w\.\-]*@\w+[\w\-]*\.[\w\.]*[a-z0-9]+', re.IGNORECASE)
    emails_in_file = list(set(map(string.lower, re_email.findall(content))))
    if emails_in_file:
        if len(emails_in_file) == 1:    return emails_in_file[0]
        else:
            end_one = re_email.search(content).end()
            if re_email.search(content, end_one+1).start() - end_one < 100:    return emails_in_file[0]
    return ''

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/resume_process_job_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    eventnotifier.sendEventNotification("Jobhunt Job Error: resume_process_job", err)

delay = 10 #seconds
conn_str = "dbname='jhindb' user='jhindbu' password='*password#' host='127.0.0.1'"
workspace_path = '/skillda/system/temp/docshare'
time_stamp_file = '/apps/jobhuntin/backslash/jobs/resume_process_job_time_stamp.txt'
pid_filepath = '/apps/jobhuntin/backslash/logs/resume_process_job.pid'

if __name__ == "__main__":
    if os.path.exists(pid_filepath):   exit()    
    try:
        with open(pid_filepath, 'w') as f:
            f.write(str(os.getpid()))
            
        convert()
    finally:
        os.remove(pid_filepath)
    
