#!/usr/bin/env python

import re, string, sys

sys.path.append('/apps/socialray/common/pylibs')
from search_client import SearchClient, IndexUpdateEntry, DataFormatter as format, DataUnformatter as unformat

regions = {'karnataka':['bangalore', 'mysore'],
                'tamil nadu':['chennai']}

CLUSTER_ID = 'backslash_resumes'

def matchResumes(keywords, experience, location, max_salary, last_time, fields='', start=0, rows=500):
    q = getMatchResumeQuery(keywords, experience, location, max_salary, last_time)
    print q
    s = SearchClient()
    response = s.search(q, fields, CLUSTER_ID, 'id', 'desc', start=start, rows=rows)
    int_fields = ['experience', 'min_salary', 'rating']
    date_fields = []
    for res in response.results:
        for fld in res.keys():
            if fld in int_fields:   res[fld] = unformat.Int(res[fld])
            elif fld in date_fields:   res[fld] = unformat.Date(res[fld])
            
    return response


def getMatchResumeQuery(keywords, experience, location, max_salary, last_time):
    keywords = [format.exactFormat(x) for x in keywords.replace(',', ' ').split() ]

    q = 'fulltext:(%s)' % fixQuery(' AND '.join(keywords))
    if experience:  q += ' AND experience:[%s TO *]' % format.Int(experience)

    location = location.lower()
    if not (location == 'any'):
        if location in regions:
            q += ' AND pref_location:(anywhere OR %s OR %s)' % (location, fixQuery(' OR '.join(regions[location])))
        else:
            q += ' AND pref_location:(anywhere OR ' + fixQuery(location) + ')'

    if max_salary > 0:
        q += ' AND min_salary:[%s TO %s]' % (format.Int(0), format.Int(max_salary))

    q += ' AND indexed_on:[' + format.Date(last_time) + ' TO *]'
    
    return q

def fixQuery(query):
    pat1 = re.compile('AND AND AND', re.IGNORECASE)
    pat2 = re.compile('AND OR AND', re.IGNORECASE)
    query = pat1.sub('AND', query)
    query = pat2.sub('OR', query)
    return query
