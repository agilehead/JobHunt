#!/usr/bin/env python
import os, sys, unittest, datetime
sys.path.append('/apps/jobhuntin/backslash')
os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
from django.db import transaction
from website import models, codejar

class ResumeTestCase(unittest.TestCase):

    def setUp(self):
        self.test_resumefile = 'Resume.doc'
        self.test_resumepath = '/test/Resume.doc'

    def tearDown(self):
        pass

    def testCreateResume(self):
        resume = codejar.user.addResume(self.test_resumefile, self.test_resumepath)
        resume.delete()

class RecruiterTestCase(unittest.TestCase):

    def setUp(self):
        self.name = 'Tommy Middlefinger'
        self.password = 'abcdefg'
        self.organization = 'Jobhunt'
        self.test_rec_email = 'email@example.com'
        self.test_keywords = 'Testing 123'
        self.experience = 5
        self.telephone = '9999999999'
        self.location = 'Bangalore'
        self.max_salary = 2000000
        self.job_title = 'Project Manager'
        self.job_company = 'Jessica\'s Fishmongers'
        self.job_desc = 'Sellling fish at a higher cost.'

    def tearDown(self):
        pass

    @transaction.commit_on_success
    def addRecruiter(self, email, password, name, organization, telephone):
        account = codejar.actions.createAccount(email, password, 'FR')
        account.save()
        rec = models.Recruiter()
        rec.account = account
        rec.key = dataplus.getUniqueId()

        rec.email = email
        rec.name = name
        rec.organization = organization
        rec.telephone = telephone

        #default values
        rec.verified = False
        rec.verified_on = datetime.datetime(1981, 1, 9) #default date min value ;)
        rec.results_last_sent_on = datetime.datetime(1981, 1, 9)   #Jes' bday -- default min date

        rec.save()

        return rec


    def addRecruiterSubscription(self, recruiter, keywords, experience, location, max_salary, job_title,
            job_company, job_desc, industry='', min_count=5):
        rec_subscr = models.RecruiterSubscription()
        rec_subscr.recruiter = recruiter
        rec_subscr.keywords = keywords
        rec_subscr.experience = experience
        rec_subscr.location = location
        rec_subscr.max_salary = max_salary
        rec_subscr.industry = industry
        rec_subscr.min_count = min_count
        rec_subscr.job_title = job_title
        rec_subscr.job_company = job_company
        rec_subscr.job_description = job_desc
        rec_subscr.results_last_sent_on = datetime.datetime(1981, 1, 9) #Jes' bday - default min datetime
        rec_subscr.save()
        #Send email notification on new filter.
        #filter_text = rec_subscr.keywords
        #if rec_subscr.experience:  filter_text += ' with %d years' % rec_subscr.experience
        #if rec_subscr.max_salary and rec_subscr.max_salary != 0:   filter_text += ' and salary expectation under Rs. %d Lakhs' % (rec_subscr.max_salary/100000)
        #if not rec_subscr.location.lower() == 'any':    filter_text += ' in ' + rec_subscr.location
        #params = {'resume_filter': filter_text,
        #        'recruiter_key': recruiter.key}
        #mailer.sendNewFilterAddedMail(recruiter.email, params)
        return rec_subscr

    def testCreateRecruiter(self):
        rec = self.addRecruiter(self.test_rec_email, self.password, self.name, self.organization, self.telephone, self.location)
        rec.delete()

    def testCreateRecruiterSubscription(self):
        rec = self.addRecruiter(self.test_rec_email, self.password, self.name, self.organization, self.telephone, self.location)
        resume_filter = self.addRecruiterSubscription(rec, self.test_keywords, self.experience, self.location, self.max_salary, self.job_title, self.job_company, self.job_desc)
        resume_filter.delete()
        rec.delete()
