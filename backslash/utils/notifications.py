#!/usr/bin/env python
import psycopg2, cPickle
import config

def addNotification(key, type, text='', data=None):
    if not text and data:   text = cPickle.dumps(data)
    connection = psycopg2.connect(config.conn_str)
    cursor = connection.cursor()
    stmt = 'INSERT INTO website_notification (key, type, text, activity_time) VALUES (%(key)s, %(type)s, %(text)s, current_timestamp);'
    cursor.execute(stmt, {'key':key, 'type':type, 'text':text})
    connection.commit()
    
def getNotificationTexts(key, type):
    stmt = """SELECT ID, TEXT FROM
            WEBSITE_NOTIFICATION
            WHERE KEY = '%s' AND
            TYPE = '%s'""" % (key, type)
    
    connection = psycopg2.connect(config.conn_str)
    cursor = connection.cursor()
    cursor.execute(stmt, {'key':key, 'type':type})
    results = cursor.fetchall()
    
    notification_texts = []
    for row in results:
        notification_texts.append({'notification_id':row[0],'text':cPickle.loads(str(row[1]))})
        
    return notification_texts
