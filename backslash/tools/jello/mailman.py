#!/usr/bin/env python
from __future__ import with_statement 

import html2text
import string, os, sys, datetime

from email import encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEAudio import MIMEAudio
import smtplib
# For guessing MIME type based on file name extension
import mimetypes
from email_content import EmailContent

# Send an HTML email with embedded images and a plain text message for
# email clients that don't want to display the HTML.
# with attachments
def sendOneWayMail(sender, recipients, subject, html_body, attachments=None, images=None, text_message=None):
    sendMail(sender, recipients, subject, html_body, attachments, images, text_message, '"Agilehead Services"<jthomas@agilehead-services.com>')

def createMail(sender, recipients, subject, html_body, attachments=None, images=None, text_message=None, reply_to=''):
    # Create the root message and fill in the from, to, and subject headers
    msgRoot = EmailContent('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = string.join(recipients, ',')
    msgRoot.preamble = 'Message from agilehead services'
    msgRoot['Reply-To'] = reply_to
    msgRoot['Sender'] = reply_to

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #TODO:Confirm
    #Rumor: Real mail systems always send plain-text alternative (Except spammers)
    if not text_message:
        text_message = html2text.html2text(html_body)
    msgText = MIMEText(text_message, _charset='iso-8859-1')
    msgAlternative.attach(msgText)

    # Adding the Html message body
    # Reference the image in the IMG SRC attribute by the ID like <img src="cid:image1">
    msgText = MIMEText(html_body, _subtype='html')
    msgAlternative.attach(msgText)

    if images:
        # Adding the images
        # images are assumed to be in this format - {'image1':'images/chad.jpg', 'image2':'images/jessy.jpg'}
        for cid, filepath in images.iteritems():
            fp = open(filepath, 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()

            # Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<' + cid + '>')
            msgRoot.attach(msgImage)

    if attachments:
        # Adding the attachments
        # Attachments are assumed to be a list of filepaths
        for filepath in attachments:
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(filepath)
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(filepath, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(filepath, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(filepath, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)
            # Set the filename parameter
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.split(filepath)[1])
            msgRoot.attach(msg)                
    return msgRoot
    
def sendMail(sender, recipients, subject, html_body, attachments=None, images=None, text_message=None, reply_to=''):
    try:
        msgRoot = createMail(sender, recipients, subject, html_body, attachments, images, text_message, reply_to)        
        
        # Send the email (this example assumes SMTP authentication is required)
        smtp = smtplib.SMTP()
        smtp.connect('smtp.live.com', 587)
        smtp.login('jthomas@agilehead-services.com', 'n3ls0n81')
        smtp.sendmail(sender, recipients, msgRoot.toMIMEMultipart().as_string())
        smtp.quit()
        
        #New smtp relay
        #import smtp_relay
        #smtp_relay.sendMail(sender, recipients, msgRoot)
        logSentMail(recipients, subject)
    except:
        logError('Sending mail failed. Recipients=' + str(recipients) + ', subject=' + subject +  ' Error:' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))

def logSentMail(recipients, subject):
    with open('logs/sentmail.txt', 'a') as file:
        file.write(str(datetime.datetime.utcnow()) + '\t' + str(recipients) + '\t' + subject + '\n')
    
def logError(err):
    with open('logs/mailman_errors.txt', 'a') as file:
        file.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')