echo checking models...
python /apps/jobhuntin/backslash/website/manage.py validate PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/
echo checking python files...
ls /apps/jobhuntin/backslash/*/*.py | PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/ DJANGO_SETTINGS_MODULE='website.settings' xargs pychecker --quiet --level Error
ls /apps/jobhuntin/backslash/website/ajax/*.py | PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/ DJANGO_SETTINGS_MODULE='website.settings' xargs pychecker --quiet --level Error
ls /apps/jobhuntin/backslash/website/codejar/*.py | PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/ DJANGO_SETTINGS_MODULE='website.settings' xargs pychecker --quiet --level Error
ls /apps/jobhuntin/backslash/website/middleware/*.py | PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/ DJANGO_SETTINGS_MODULE='website.settings' xargs pychecker --quiet --level Error
ls /apps/jobhuntin/backslash/website/views/*.py | PYTHONPATH=$PYTHONPATH:/apps/jobhuntin/backslash/ DJANGO_SETTINGS_MODULE='website.settings' xargs pychecker --quiet --level Error
