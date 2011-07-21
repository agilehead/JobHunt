#!/bin/sh
sql_file="/home/chad/resume-set-"`eval date +%Y%m%d%H%M%S`".sql"
gzip_file="/home/chad/backup/jobhunt-"`eval date +%Y%m%d%H%M%S`".tar.gz"
pg_dump -d jhindb -U jhindbu -W > $sql_file
sudo tar -cvf - /apps/jobhuntin/backslash/data/resumes/ $sql_file | gzip -c > $gzip_file
rm $sql_file


