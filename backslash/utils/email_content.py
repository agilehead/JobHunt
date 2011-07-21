#!/usr/bin/env python

from email.MIMEMultipart import MIMEMultipart

class EmailContent(dict):
    
    def __init__(self, type='related'):
        self.type = type
        self.type = 'related'
        self.attachments = []    
        
    def attach(self, something):
        self.attachments.append(something)
        
    def toMIMEMultipart(self):
        msg = MIMEMultipart(self.type)        
        for key in self:
            msg[key] = self[key]
            
        for a in self.attachments:
            msg.attach(a)
            
        return msg