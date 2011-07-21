#!/usr/bin/env python
from django.http import HttpResponse
from django.utils import simplejson 

def getFailureResp(reason, desc=''):
    result = {}
    result['info'] = reason
    result['description'] = desc
    result['result'] = 'failure'
    response = HttpResponse(simplejson.dumps(result), mimetype='application/javascript')
    response['Pragma'] = 'no-cache'
    response['Cache-Control'] = 'must-revalidate'
    response['Cache-Control'] = 'no-store'
    response['Cache-Control'] = 'no-cache'
    return response

def getSuccessResp(reason, desc=''):
    result = {}
    result['info'] = reason
    result['description'] = desc
    result['result'] = 'success'
    response = HttpResponse(simplejson.dumps(result), mimetype='application/javascript')
    response['Pragma'] = 'no-cache'
    response['Cache-Control'] = 'must-revalidate'
    response['Cache-Control'] = 'no-store'
    response['Cache-Control'] = 'no-cache'
    return response