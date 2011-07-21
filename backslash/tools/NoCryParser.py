#!/usr/bin/env python

import os, re, string, sys

def parseFiles(source_folder, output_file, all_values):
    re_cleanup = re.compile('=\r?\n')
    re_name = re.compile('\<title\>(.*?)\-', re.IGNORECASE)
    re_email = re.compile('\w+[\w\.\-]*@\w+[\w\-]*\.[\w\.]*', re.IGNORECASE)
    re_phone = re.compile('\<img[^\>]*phone\.gif\"\s*\>([^\<]*)\<', re.IGNORECASE)
    re_workExp = re.compile('\<strong\>Work Experience\<\/strong\>\<\/td\>\<td[^\>]*\>\:\<\/td\>\<td[^\>]*\>\<p\>([^\<]*)\<\/p\>', re.IGNORECASE)
    re_keySkills = re.compile('Key\sSkills\:(.*?)\<\/td\>', re.IGNORECASE)
    re_cleanSpan = re.compile('\<\/*span[^\>]*\>', re.IGNORECASE)
    re_cleanLine = re.compile('\r?\n')
    
    
    list = []
    for file in os.listdir(source_folder):
        try:
            if not file.endswith('.mht'):	pass
            file_path = os.path.join(source_folder, file)
            if not os.path.isfile(file_path): pass
            
            f = open(file_path)
            content = f.read()
            f.close()
    
            #content = re_cleanup.sub('', content)
            #email = string.split(re_email.findall(content)[0], ',')[0].strip()
            content = content.replace('\r\n','\n').replace('=\n', '')
            m = re_email.search(content)
            if m:
                email = content[m.start(0):m.end(0)]
            else:
                raise Exception('Email not found in ' + file_path)
            name = re_name.findall(content)[0].strip()
            #if all_values:
            #    fields.append(re_phone.findall(content)[0].strip())
            #    fields.append(re_workExp.findall(content)[0].strip())
            #    #fields.append(re_cleanSpan.sub('', re_keySkills.findall(content)[0].strip()))
            
            line = re_cleanLine.sub('', email + ';name=' + name)
            list.append(line)
            print line
            #list.append(string.join([re_cleanLine.sub('',x) for x in fields], ';'))
            #raise Exception('stopped..')
        except:
            print str(sys.exc_info()[1])
    

    f = open(output_file, 'w')
    for line in list:   f.write(line + '\n')
    f.close()

if __name__ == "__main__":
    args = sys.argv

    all_values = False
    source_folder = ''
    output_file = 'output.txt'
    
    try:
        if len(args) < 3:   raise Exception('Invalid arguments.')
        i=1
        while i < len(args):
            if args[i] == "-all":
                all_values = True
            elif args[i] == "-s":
                source_folder = args[i+1]
                if not os.path.isdir(source_folder):
                    raise Exception('The source folder does not exist.')
                i+=1
            elif args[i] == "-o":
                output_file = args[i+1]
                i+=1
            i+=1
        
        parseFiles(source_folder, output_file, all_values)   
    except Exception, err_msg:
        print 'Error:', err_msg
        print 'Usage: NoCryParser.py -s source folder [-o output file] [-all]'
