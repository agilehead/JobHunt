from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response

import base64, urllib, cPickle, datetime, re, string
from utils import search_helper, dataplus
from website import models, codejar

page_size = 20
def handle(request):
    rec, redirect = codejar.actions.handleSecurity(request, 'recruiter')
    if not rec:	return redirect

    page = dataplus.dictGetVal(request.REQUEST, 'page', 0, string.atoi)
    subscr_id = dataplus.dictGetVal(request.REQUEST, 'sub_id', 0, string.atoi)
    keywords = dataplus.dictGetSafeVal(request.REQUEST, 'keywords', '')
    search_tuple = dataplus.dictGetSafeVal(request.REQUEST, 'searchTuple', '')
    search_dict = {}
    min_datetime = datetime.datetime(1981, 1, 9)    #Jes B'day
    response = None
    search_desc = ''
    if subscr_id:    
        subscr = dataplus.returnIfExists(models.RecruiterSubscription.objects.filter( id=subscr_id))
        if not (subscr and subscr.recruiter == rec):	raise Http404
        search_dict = {'keywords':subscr.keywords, 'experience':subscr.experience, 'location':subscr.location,
                       'max_salary':subscr.max_salary, 'limit_time':subscr.results_last_sent_on}
    elif keywords:
        experience = dataplus.dictGetVal(request.REQUEST, 'experience', 0, string.atoi)
        location = dataplus.dictGetSafeVal(request.REQUEST, 'location', 'Any')
        max_salary = dataplus.dictGetVal(request.REQUEST, 'maxSalary', 0, string.atoi)
        search_tuple = base64.b64encode(cPickle.dumps((keywords, experience, location, max_salary)))
        search_dict = {'keywords':keywords.strip('\r'), 'experience':experience, 'location':location.strip('\r'),
                       'max_salary':max_salary, 'limit_time':min_datetime}
        models.RecruiterData.addToRecentSearches(rec, search_dict)
    elif search_tuple:
        search_keywords, experience, location, max_salary = cPickle.loads(base64.b64decode(search_tuple))
        search_dict = {'keywords':search_keywords, 'experience':experience, 'location':location,
                       'max_salary':max_salary, 'limit_time':min_datetime}
    else:
        raise Http404
    
    response = search_helper.matchResumes(search_dict['keywords'], search_dict['experience'], search_dict['location'], search_dict['max_salary'], search_dict['limit_time'], start=page * page_size, rows=page_size)
    user_list = response.results
    num_pages = 0
    if (len(user_list) > 0):
    	num_pages = ((string.atoi(response.numFound )-1) / page_size) + 1
    
    return codejar.actions.render(request, 'recruiters/searchresults.htm', {'subscription_id':subscr_id,
                              'search_tuple': search_tuple,
                              'search_url': urllib.urlencode(search_dict),
                              'users': addFormatting(user_list, page),
                              'search_desc': getSearchDisplay(search_dict),
                              'links_html': getLinksHtml(num_pages, page, user_list),
                              'num_results':response.numFound,
                              'date':datetime.datetime.utcnow().strftime('%B %e, %Y')
                              })

def getSearchDisplay(search_dict):
    display_str = search_dict['keywords']
    if search_dict['experience']:   display_str += ' with %d years' % search_dict['experience']
    if not search_dict['location'].lower() == 'any':   display_str += ' in %s' % search_dict['location']
    return display_str

def addFormatting(users, page):
    idx = page * page_size + 1
    for usr in users:
        min_salary_desc = ''
        usr['index'] = idx
        if usr['min_salary']:    usr['min_salary'] = '%d Lakhs' % (usr['min_salary']/100000)
        #Software Engineer with Helzinger Consulting, 7 years exp, in Bangalore.
        usr['profile_info'] = ('Fresher', "%s with %s, %d years of experience." % (usr['curr_designation'], usr['curr_employer'], usr['experience']))[usr['experience'] > 0]

        if usr['summary']:
            summary_html =  string.join([x.strip() for x in re.split('\n+', re.sub('\r?\n', '\n', usr['summary'])) if re.match('[a-zA-Z]{2,}', x.strip())], ' <strong> | </strong> ') + '.'
            #summary_html = string.join(usr['summary'].split('\n'), ' <strong> | </strong> ') + '.'
            if len(summary_html) > 300: summary_html = summary_html[:297] +'...'
            if summary_html.rfind('<strong>') > summary_html.rfind('</strong>'):   summary_html = summary_html[:summary_html.rfind('<strong>')].strip() + '...'
            usr['summary'] = summary_html
        usr['indexed_on'] = datetime.datetime.strptime(usr['indexed_on'], '%Y%m%d%H%M%S').strftime('%d %b %Y')
        usr['is_premium_user'] = (usr['account_type'] == 'PU')
        idx += 1

    return users

def getLinksHtml(num_pages, curr_page, users):
    html =''
    if users:
        html = '<select name="pageselect" id="pageselect" onchange="javascript:getPage($(\'pageselect\').value);">\n'
        for i in range(num_pages):
            if i == curr_page:
                html += '<option value="'+ str(i) + '" selected="selected">Page ' + str(i+1) + '</option>\n'
            else:
                html += '<option value="'+ str(i) + '">Page ' + str(i+1) + '</option>\n'
        html += '</select> '

        if curr_page:
            html += '<a href="javascript:getPage(' + str(curr_page-1) + ');">... </a>\n '
        for i in range(num_pages):
            if i == curr_page:
                html += str(i+1) + ' '
            else:
                html += '<a href="javascript:getPage(' + str(i) + ');">' + str(i+1) + '</a>\n '
        if curr_page < num_pages -1:
            html += '<a href="javascript:getPage(' + str(curr_page+1) + ');"> ...</a>\n '

    return html
