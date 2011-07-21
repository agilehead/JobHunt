#!/usr/bin/env python
from __future__ import with_statement
from django.http import HttpResponse, Http404
from django.db import transaction

import os, sys, datetime, random, time
from website import models
from utils import dataplus, eventnotifier

doc_save_dir = '/apps/jobhuntin/data/resumes'
    
def saveResumeFile(data):
    doc_filepath = getNewFilepath()
    with open(doc_filepath, 'wb') as f:
        f.write(data)
    return doc_filepath    
    
def getNewFilepath():
    target_dir = doc_save_dir + '/' + time.strftime("%d%m%Y", time.gmtime())
    if not os.path.exists(target_dir):  os.mkdir(target_dir)
    return target_dir + '/' + dataplus.getUniqueId() + '.doc'

def saveUploadedResume(request, resume_field_name):
    try:
        if not request.FILES:
            return '', '', 'upload_file_not_found'
        
        file = request.FILES[resume_field_name]
        ext = os.path.splitext(file.name.lower())[1]
        if (ext not in ['.doc', '.docx']):# For later - ['.doc', '.rtf', '.htm', '.html']
            return '', '', 'unsupported_doctype_upload'
        
        content = file.read()
        if len(content) > 1048576:  #1 MB is the current limit
            return '', '', 'large_doc_upload'
        
        try:
            resume_path = saveResumeFile(content)
        except:
            logError('Writing uploaded resume file failed : ' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))
            return '', '', 'unknown'#'cannot_write_document'
        
        return file.name, resume_path, ''
    except:
        logError('Save resume doc failed : ' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))
        return '', '', 'unknown'
    
def addFreeUserWithResume(request, resume_field_name):
    uploaded_filename, doc_filepath, error_id = saveUploadedResume(request, resume_field_name)
    if not error_id:
        user = addFreeUser(uploaded_filename, doc_filepath)
        return user.key, ''
    else:
        return '', error_id
    
@transaction.commit_on_success
def addPremiumUser(name, email, password, telephone):
    user_key = dataplus.getUniqueId()
    proxy_email = generateAnonMailId()
    user = models.User.create(email, password, 'PU', user_key, name, email, telephone, proxy_email=proxy_email)
    user.account.account_state = 'I'
    user.account.save()
    
    return user

@transaction.commit_on_success
def addFreeUser(doc_filename, doc_filepath):
    user_key = dataplus.getUniqueId()
    user = models.User.create(user_key, dataplus.getUniqueId(), 'FU', user_key, doc_filename=doc_filename, doc_filepath=doc_filepath, resume_updated_on=datetime.datetime.utcnow())    
    return user

def logError(err):
    with open('/apps/jobhuntin/logs/resume_save_errors.txt', 'a') as file:
        file.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    eventnotifier.sendEventNotification("Jobhunt Job Error: resume_process_job", err)
        
def downloadResume(user, format):
    mime_type = {'doc':'application/msword', 'html':'text/html'}[format]
    resume_filepath = {'doc':user.doc_filepath, 'html':user.html_filepath}[format]
   
    if resume_filepath and os.path.exists(resume_filepath):        
        f = open(resume_filepath)
        content = f.read()
        f.close()
        
        filename = (user.doc_filename[:user.doc_filename.rindex('.')+1] + format, user.doc_filename)[format == 'doc']
        response = HttpResponse(content, mimetype=mime_type)
        if not format == 'html':    response['Content-Disposition'] = 'attachment; filename=' + filename
        return response
    else:
        raise Http404
    
def generateAnonMailId(length=8):
    allowedChars = "0123456789"
    
    def getEmail():
        word = ""
        for i in range(0, length):
            word = word + allowedChars[random.randint(0,0xffffff) % len(allowedChars)]
        return 'anon' + word + '@jobhunt.in'
    
    email = getEmail()
    while models.User.objects.filter(proxy_email=email):
        email = getEmail()
        
    return email
    
    
  