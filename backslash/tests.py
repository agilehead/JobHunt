import unittest
from utils import mailer_test, smtp_relay_test, mailman_test
from tests import core


if __name__ == "__main__":
    mailer_suite = []
    for cls in mailer_test.MailerTestCase, smtp_relay_test.SmtpRelayTestCase, mailman_test.MailmanTestCase, core.ResumeTestCase, core.RecruiterTestCase:
        mailer_suite += [unittest.TestLoader().loadTestsFromTestCase(cls)]

    #add all suites to be run.
    all_tests = unittest.TestSuite(mailer_suite)

    unittest.TextTestRunner(verbosity=2).run(all_tests)
