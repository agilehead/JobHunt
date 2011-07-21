#!/usr/bin/env python

import mailer
import unittest

class MailerTestCase(unittest.TestCase):
    
    def setUp(self):
        self.test_email = 'jeswin@gmail.com'
    
    def tearDown(self):
        pass

    def testSendResumeAddedMail(self):
        params = {'name': 'James Bonda',
                'resume_key': '007'}
        mailer.sendResumeAddedMail(self.test_email, params)
        
    def testSendNewFilterAddedMail(self):
        params = {'resume_filter': 'Snake Charmer',
                'recruiter_key': '007'}
        mailer.sendNewFilterAddedMail(self.test_email, params)
        
if __name__ == '__main__':
    unittest.main()
