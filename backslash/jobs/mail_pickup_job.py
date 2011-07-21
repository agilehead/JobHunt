#!/usr/bin/env python
from __future__ import with_statement
import email, poplib, re, datetime, psycopg2, os, time, sys, string
sys.path.append('/apps/jobhuntin/backslash')
from utils import mailman, mailer, dataplus, eventnotifier

error_count_log = '/apps/jobhuntin/backslash/logs/mail_pickup_error_count.log'

def saveEmailedResumes():
    global error_count
    pop = poplib.POP3(pop_server)
    pop.user(pop_user)
    pop.pass_(pop_pass)
    stats = pop.stat()
    rx_headers = re.compile('^(From|To|Subject|Content-Type):',re.IGNORECASE)
    
    if stats and stats[0] > 0:  
        connection = psycopg2.connect("dbname='jhindb' user='jhindbu' password='*password#' host='127.0.0.1'")
        cursor = connection.cursor()
        
        time_now = datetime.datetime.utcnow()
        count = stats[0]
        for i in range(1,1+count):
            try:
                resp, lines, bytes = pop.top(i,10)
                req_lines = filter(rx_headers.match, lines)
                headers = map(lambda x: x.split(': ', 1), req_lines)
                
                def find_in_headers(hdr_name):
                    res = filter(lambda x: x[0].lower() == hdr_name.lower(), headers)
                    if len(res) > 0:    return res[0][1]
                    else:   return ''
                
                doc_filename = None
                doc_filepath = None
                has_doc = False
                if find_in_headers('Content-Type').lower().startswith('multipart'):
                
                    msg = email.message_from_string('\n'.join(pop.retr(i)[1]))
                    body = {'html':'', 'plain':''}
                    for part in msg.walk():
                        if part.get_content_maintype() == 'text':
                            sub_type = part.get_content_subtype()
                            if sub_type in ['plain','html']:
                                data = dataplus.decode(part.get_payload(decode=True))
                                if len(data) < 25:  pass
                                body[sub_type] = data
                        
                        if part.get_content_maintype() == 'application' and part.get_content_subtype() == 'msword':
                            doc_filepath = saveResumeFile(part.get_payload(decode=True))
                            doc_filename = part.get_filename()
                            has_doc = True
                    
                    if doc_filename:
                        stmt = "INSERT INTO website_receivedmail (from_address, subject, body_html, body_text, doc_filepath, received_on)"
                        stmt += " VALUES (%(from_address)s, %(subject)s, %(html_body)s, %(plain_body)s, %(doc_filepath)s, %(time_now)s)"
                        cursor.execute(stmt, {'from_address':find_in_headers('From')[:100], 'subject':find_in_headers('Subject')[:100],
                                            'html_body':body['html'], 'plain_body':body['plain'],
                                            'doc_filepath':doc_filepath, 'time_now':str(time_now)})
                        cursor.execute("SELECT CURRVAL('website_receivedmail_id_seq');")
                        mail_id = str(cursor.fetchone()[0])
                        resume_key = dataplus.getUniqueId()
                        
                        stmt = 'INSERT INTO website_resume (doc_filename, doc_filepath, html_filepath, text_filepath, doc_hash, posted_on, mail_ref_id, "name", email, experience, tags, industry, "location", current_employer, summary, "key", tagged, is_active, min_salary, desired_employer) '
                        stmt += "VALUES (%(doc_filename)s ,%(doc_filepath)s, '', '', '', %(time_now)s, %(mail_id)s, '', '', 0, '', '', '', '', '', %(resume_key)s, False, False, 0, '')"
                        cursor.execute(stmt, {'doc_filename':doc_filename, 'doc_filepath':doc_filepath, 'time_now':str(time_now), 'mail_id':mail_id, 'resume_key':resume_key})
                    
                from_hdr = find_in_headers('From')
                candidate_name = getNameFromHeader(from_hdr)
                if has_doc:
                    params = {'name':candidate_name, 'resume_key': resume_key}
                    mailer.sendResumeReceivedMail(from_hdr, params)
                    eventnotifier.sendEventNotification('New Resume by mail: %s posted on: %s' % (doc_filename, time_now.strftime('%d/%m/%Y %H:%M:%S %p')))
                else:
                    params = {'name': candidate_name}
                    mailer.sendInvalidResumeMail(from_hdr, params)
                
                pop.dele(i)
                    
            except:
                error_count += 1
                setErrorCount(error_count)
                logError('Processing mail ' + find_in_headers('From') + ' - ' + find_in_headers('Subject') + ' failed : ' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))
                if error_count == max_errors:
                    logError('Jobhunt Job Error: Stopping mail_pickup_job as it has encountered Maximum number of errors.')
                    break
                
        connection.commit()
    pop.quit()
    
def getNewFilepath():
    target_dir = doc_save_dir + '/' + time.strftime("%d%m%Y", time.gmtime())
    if not os.path.exists(target_dir):  os.mkdir(target_dir)
    return target_dir + '/' + dataplus.getUniqueId() + '.doc'
    
def saveResumeFile(data):
    doc_filepath = getNewFilepath()
    with open(doc_filepath, 'wb') as f:
        f.write(data)
    return doc_filepath
    
def getNameFromHeader(from_text):
    if from_text.find('<') > -1:
        return from_text[:from_text.find('<')].strip().strip('"')
    else:
        return from_text[:from_text.find('@')].strip()

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/mail_pickup_job_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    eventnotifier.sendEventNotification("Jobhunt Job Error: mail_pickup_job", err)

def getErrorCount():
    error_count = 0
    if os.path.exists(error_count_log):
        with open(error_count_log) as f:
            error_count = string.atoi(f.read())
    return error_count

def setErrorCount(error_count):
    with open(error_count_log, 'w') as f:
        f.write(error_count)

pop_server = 'localhost'
pop_user = 'mailreader'
pop_pass = '*password#'
doc_save_dir = '/apps/jobhuntin/backslash/data/resumes'
pid_filepath = '/apps/jobhuntin/backslash/logs/mail_pickup_job.pid'
error_count = 0
max_errors = 5

if __name__ == "__main__":
    if os.path.exists(pid_filepath):   exit()    
    try:
        with open(pid_filepath, 'w') as f:
            f.write(str(os.getpid()))
        
        error_count = getErrorCount()
        if (error_count < max_errors):
            saveEmailedResumes()
    finally:
        os.remove(pid_filepath)
    