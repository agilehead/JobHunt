#!/usr/bin/env python

from __future__ import with_statement
import datetime, string, sys
from solr import *

class SearchClient(object):

    SOLR_URL = 'http://127.0.0.1:8080/solr'

    FIELD_CLUSTER = 'clusterid'
    FIELD_DOC_ID = 'docid'

    def search(self, q, fields_to_return, clusterid, sort=None, sort_order="asc", **params):
        q += ' AND ' + SearchClient.FIELD_CLUSTER + ':' + clusterid
        s = SolrConnection(SearchClient.SOLR_URL)
        return s.query(q, fields_to_return, sort=sort, sort_order=sort_order, **params)

    #entries are of type IndexUpdateEntry
    def updateIndexes(self, entries, clusterid):
        s = SolrConnection(SearchClient.SOLR_URL)

        #implement solypy batching...
        #Note: batching will throw error if there are multiple updates on same id within the same batch

        for entry in entries:
            try:
                if entry.type == 'update':
                    doc = {}
                    doc[SearchClient.FIELD_CLUSTER] = clusterid
                    doc[SearchClient.FIELD_DOC_ID] = clusterid + '_' + entry.id
                    doc.update(entry.fields.items())
                    s.add_many([doc])
    
                if entry.type == 'delete':
                    s.delete(entry.id)
    
                s.commit()
            except:
                logError(entry.type + ' index to solr failed for "' + str(entry.id) + '" : ' + str(sys.exc_info()[0]) + ', ' + str(sys.exc_info()[1]))

def logError(err):
    with open('/apps/jobhuntin/backslash/logs/search_client_errors.txt', 'a') as f:
        f.write(str(datetime.datetime.utcnow()) + '\t' + err + '\n')
    #eventnotifier.sendEventNotification("Jobhunt Job Error: trinity_feed_job", err)

#ints to be stored as '000000
class DataFormatter(object):

    INT_MAX = '9' * 32
    DATE_MAX = '999999999999'

    #does not support negative integers yet..
    @staticmethod
    def Int(num):
        INT_LEN = 32
        num = str(num)
        return ('0' * (INT_LEN - len(num))) + num

    @staticmethod
    def Date(d):
        return d.strftime("%Y%m%d%H%M%S")

    @staticmethod
    #This
    def exactFormat(str):
        special_chars = [('#', 'hash'), ('+', 'plus'), ('-', 'dash')]

        for c,alt in special_chars:
            str = str.replace(c, '__' + alt + '__')

        return str

#ints to be stored as '000000
class DataUnformatter(object):

    #does not support negative integers yet..
    @staticmethod
    def Int(str_num):
        return string.atoi(str_num)

    @staticmethod
    def Date(str_date):
        return datetime.datetime.strptime(str_date, "%Y%m%d%H%M%S")

    @staticmethod
    #This
    def exactFormat(str):
        special_chars = [('#', 'hash'), ('+', 'plus'), ('-', 'dash')]

        for c,alt in special_chars:
            str = str.replace('__' + alt + '__', c)

        return str

class IndexUpdateEntry(object):
    def __init__(self, typeOfUpdate, id, fields=None):
        self.type = typeOfUpdate
        self.id = id
        self.fields = fields
