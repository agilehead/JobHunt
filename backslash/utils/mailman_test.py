#!/usr/bin/env python

import smtp_relay
import unittest

class MailmanTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def testMailman(self):
        #New smtp relay\
        import mailman
        mailman.sendMail('Jobhunt.in<mailmana@job-huntin.com>', ['jeswin@gmail.com'], 'This is a unit test', '<div><h1>Hello, World</h1><p>This is a unit test.</p></div>')
    
if __name__ == '__main__':
    unittest.main()
