#!/usr/bin/env python

import smtp_relay
import unittest

class SmtpRelayTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
        
    def testRelay(self):
        #New smtp relay\
        import mailman
        msgRoot = mailman.createMail('Jobhunt.in<mailmana@job-huntin.com>', ['jeswin@gmail.com'], 'This is a unit test', '<div><h1>Hello, World</h1><p>This is a unit test.</p></div>', 
            attachments=None, images=None, text_message=None, reply_to='')
        smtp_relay.sendMail('Jobhunt.in<mailmana@job-huntin.com>', ['jeswin@gmail.com'], msgRoot)


if __name__ == '__main__':
    unittest.main()
