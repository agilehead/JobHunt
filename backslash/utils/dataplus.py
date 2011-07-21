#!/usr/bin/env python
import cgi, datetime, hashlib, random, types

default_encoding = 'ascii'

def dictGetSafeVal(dict, key, otherwise = None, converter = None, encoding=default_encoding):
    return dictGetVal(dict, key, otherwise, converter, True, encoding)

def dictGetVal(dict, key, otherwise = None, converter = None, escapeHtml = False, encoding=None):
    try:
        result = dict[key]
    except:
        return otherwise
    
    if result and type(result) == types.StringType:
        result = result.strip()

    if encoding:
        result = decode(result, encoding)    
    
    if converter:
        result = converter(result)
    
    if escapeHtml:
        result = cgi.escape(result, True)
           
    return result

def decode(text, encoding=default_encoding, action='ignore'):
    try:
        return text.decode(encoding, action)
    except:
        #That didn't work.
        possible_encodings = ['latin-1', 'utf-8', 'utf-16', 'ascii']
        for enc in possible_encodings:
            if enc != encoding: #we have already tried this, not again!
                try:
                    return text.decode(enc, action)
                except:
                    pass

def getPreviewText(text, max_length=200, offset=0):
    try:
        if len(text[offset:]) > max_length:
            return text[offset:offset + max_length-3] + '...'
        else:
            return text
    except:
        return ''

def getUniqueId(length=12):
    allowedChars = "abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWZYZ0123456789"
    word = ""
    for i in range(0, length):
        word = word + allowedChars[random.randint(0,0xffffff) % len(allowedChars)]
    return word
    
def returnIfExists(query_set):
    if query_set.count() > 0:
        return query_set[0]

def hash(input):
    md5 = hashlib.md5()
    md5.update(input)
    return md5.hexdigest()

def toAscii(text, action='ignore'):
    return text.encode('ascii', action)
    
def getOrderedList(dict, ordered_keys):
    return [dict[key] for key in ordered_keys if dict.has_key(key)]
    
def getNewOrderId(length=12):
    allowedChars = "0123456789"
    word = ""
    for i in range(0, length):
        word = word + allowedChars[random.randint(0,0xffffff) % len(allowedChars)]
    return "JH-" + datetime.datetime.now().strftime("%Y%b%d") + "/" + word
