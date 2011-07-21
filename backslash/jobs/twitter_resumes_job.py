#!/usr/bin/env python
import sys, pycurl, psycopg2

sys.path.append('/apps/jobhuntin/backslash')
from utils import config

url_update='http://twitter.com/statuses/update.json'
url_credverify='http://twitter.com/account/verify_credentials.json'
uidpwd='jobhuntinresume:*password#'

#just to test 
def verifyTwitterCredentials():
	c = pycurl.Curl()
	c.setopt(c.URL, url_credverify)
	c.setopt(c.USERPWD, uidpwd)
	twitterfeed = c.perform()
  
	status = c.getinfo(c.HTTP_CODE)
				    
	if str(status) == '200':
		verified = True
	else:
		verified = False
		c.close()
			
	print (verified)

def sendResumeTweets():
	stmt = """SELECT KEY, TAGS FROM WEBSITE_USER WHERE 
		TAGGED_ON BETWEEN CURRENT_TIMESTAMP - interval '5 mins' AND CURRENT_TIMESTAMP
		OR RESUME_UPDATED_ON BETWEEN CURRENT_TIMESTAMP - interval '5 mins' AND CURRENT_TIMESTAMP
		AND TAGS <> ''"""
	cursor.execute(stmt)
	results = cursor.fetchall()

	if results:
		for row in results:
			msg = 'http://www.jobhunt.in/res/' + row[0] + ' >>' + row[1]
			if len(msg) > 140: msg = msg[0:139]
			print ('tweeting: ' + msg)
			tweet(msg)
	else:
		print('Nothing to tweet')

def tweet(msg):
	status = 'status=' + msg 
	c = pycurl.Curl()
	c.setopt(c.URL, url_update)
	c.setopt(c.USERPWD, uidpwd)
	c.setopt(c.POST, 1)
	c.setopt(c.POSTFIELDS, status)
	c.perform()
	c.close()

connection = psycopg2.connect(config.conn_str)
cursor = connection.cursor()

if __name__ == "__main__":
	#verifyTwitterCredentials()
	sendResumeTweets()
	
