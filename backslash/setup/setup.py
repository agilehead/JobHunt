#!/usr/bin/env python

import os

def makeWritableDirs(list):
    for dir in list:
        failableExec('mkdir ' + dir)
        failableExec('chmod 777 ' + dir)

def failableExec(cmd):
    try:
        os.system(cmd)
    except:
        pass;

if __name__ == "__main__":
    dirs = ['/apps/jobhuntin/backslash/data',
            '/apps/jobhuntin/backslash/data/resumes',
            '/apps/jobhuntin/backslash/logs'
        '/apps/jobhuntin/backslash/logs/smtprelay']
    makeWritableDirs(dirs)
