#!/usr/bin/env python
import sys, datetime

sys.path.append('/apps/jobhuntin/backslash')
sys.path.append('/apps/jobhuntin/backslash/website')

from django.core.management import setup_environ
from website import settings

setup_environ(settings)

from website import models
from utils import dataplus

recruitersList = [
('Guru Prasad', 'EFOX Software Solutions Pvt Ltd', 'guru.p@efoxsystems.com'), 
('Haritha','EFOX Software Solutions Pvt Ltd', 'haritha.g@efoxsystems.com'), 
('Shahizas','Options Consultancy', 'shahizas@optionsconsultancy.com'), 
('Neetu Makhija','Abyss & Horizon Consulting Pvt Ltd', 'neetu@ahcindia.com'), 
('Ameena','Globalhunt.in', 'ameena@globalhunt.in'), 
('Preethi Ramesh','Accenture', 'preethi.ramesh@accenture.com'), 
('Sanober Zia','Wizmatrix Consulting', 'consultant9@wizmatrix.com'), 
('Huda','Vertex Corporate Services', 'huda@vertexcorp.net'),
('Sanober Zia','Wizmatrix Consulting', 'consultant9@wizmatrix.com'), 
]

def createRecruiters():
    for rec in recruitersList:
        addRecruiter(rec[2], rec[0], rec[1])
    
def addRecruiter(email, name, organization):

    print('creating Recruiter ' + email + ' ' + name + ' ' + organization)

    account = models.Account()
    account.username = email
    account.password = dataplus.hash(dataplus.getUniqueId())
    account.account_type = 'FR'
    account.account_state = 'I'
    
    account.email_verified = True
        
    account.save()

    rec = models.Recruiter()
    rec.account = account
    rec.key = dataplus.getUniqueId()

    rec.email = email
    rec.name = name
    rec.organization = organization
    rec.telephone = ''

    #default values
    rec.verified = True #only through invites
    rec.verified_on = datetime.datetime(1981, 1, 9) #default date min value ;)
    rec.results_last_sent_on = datetime.datetime(1981, 1, 9)   #Jes' bday -- default min date

    rec.save()
    
    models.RecruiterData(recruiter=rec).save()
    
    models.Token.getNew(email, type='RecPropaganda')

    return rec

if __name__ == "__main__":
    createRecruiters()
    
    
