from django.http import HttpResponseRedirect

import datetime, cPickle, string
from website import models, codejar
from utils import dataplus, hotmetal
from website.codejar import html_options

def handle(request):
    user, redirect = codejar.actions.handleSecurity(request, 'user')
    if not user:    return redirect

    if request.method == 'GET':
        prof_views = models.Notification.objects.filter(key=str(user.id), type='ProfViewed')
        last_month_date = datetime.datetime.today()-datetime.timedelta(days=30)

        total_prof_view_count = 0
        total_prof_view_recs = []
        this_month_prof_view_count = 0
        this_month_prof_view_recs = []
        for item in prof_views:
            total_prof_view_count += 1
            rec_id = cPickle.loads(str(item.text))['recruiter_id']
            if not rec_id in total_prof_view_recs: total_prof_view_recs.append(rec_id)

            if item.activity_time > last_month_date:
                this_month_prof_view_count += 1
                if not rec_id in this_month_prof_view_recs: this_month_prof_view_recs.append(rec_id)

        reports = models.Notification.objects.filter(key=str(user.id), type='UserReport').order_by('-activity_time')[:5]
        user_reports = []
        for rept in reports:
            user_reports.append((getWeekName(rept.activity_time), rept.activity_time.strftime("%Y%m%d")))

        dict = {'user':user,
                'total_prof_views':total_prof_view_count,
                'total_prof_view_recs':len(total_prof_view_recs),
                'this_month_prof_views':this_month_prof_view_count,
                'this_month_prof_view_recs':len(this_month_prof_view_recs),
                'user_reports':user_reports,
                'settings_view_html':getSettingsDisplayHtml(user),
                'settings_edit_html':getSettingsEditHtml(user),
                }
        return codejar.actions.render(request, 'dashboard.htm', dict)
    elif request.method == 'POST':
        pass

def getSettingsDisplayHtml(user):
    html = """
                                <p>
                                    %s <span class="link edit small" onclick="javascript:editSection('isJobHunting')">
                                       Change</span>
                                </p>
                                <h2>Profile Information</h2>
                                <div class="editSectionLink">
                                    <span class="link edit" onclick="javascript:editSection('personalInfo')">
                                        Edit profile information</span></div>
                                <div class="para condensed">
                                    %s
                                </div>
                                <h2>Job Preferences</h2>
                                <div class="editSectionLink">
                                    <span class="link" onclick="javascript:editSection('jobPreferences')">
                                        Edit job preferences</span></div>
                                <div class="para condensed">
                                    %s
                                </div>
                                <h2>Anonymous Summary</h2>
                                <div class="editSectionLink">
                                    <span class="link edit" onclick="javascript:editSection('summary')">
                                        Edit summary</span></div>
                                    %s
                                <p class="small"><a href="/viewsummary.htm">Preview summary</a> as seen by recruiters.
                                </p>
                                """ % (getJobInterestDisplay(user), getPersonalInfoDisplay(user), getJobPrefDisplay(user), getSummaryDisplay(user))
    return html

def getSettingsEditHtml(user):
    html = """
                    <div id="isJobHunting_edit" class="section">
                        <h2>
                            Make resume available to recruiters?</h2>
                        <p>
                            %s
                        </p>
                    </div>
                    <div id="personalInfo_edit" class="section">
                        <h2>
                            Personal Information</h2>
                            %s
                    </div>
                    <div id="jobPreferences_edit" class="section">
                        <h2>
                            Job Preferences</h2>
                            %s
                    </div>
                    <div id="summary_edit" class="section">
                        <h2>
                            Anonymous Summary</h2>
                        <p>
                            <span class="warn">DO NOT include any details which could be used to identify you.</span>
                            <br />
                            <em>Focus on your skills and accomplishments</em>. See these samples:<br />
                            - (sample) As Business Development Manager, grew sales by $4 million in 2007-2008.<br />
                            - (sample) PMI Certified Project Manager, managed teams of upto 50 members.<br />
                        </p>
                        <div id="summaryEditBlock">%s</div>
                        <img src="/images/add.gif" alt="add" />
                        <a href="javascript:addMoreSummary();">Add some more</a>
                    </div>""" % (getIsResumeVisibleSelectHtml('isJobHunting', user.is_job_hunting),
                                getPersonalInfoEdit(user), getJobPrefEdit(user), getSummaryEdit(user))
    return html

def getSummaryDisplay(user):
    summary_html = '<em class="warn">Summary not created yet.</em>'
    if user.summary:
        summary_lines = user.summary.split('\n')
        summary_html = '<ul>\n' + reduce(lambda x,y: x + '<li class="small">' + y + '</li>\n', summary_lines, '') + '</ul>'
    return summary_html

def getSummaryEdit(user):
    edit_boxes = ''
    summary_box_count = 0

    if user.summary:
        summary_lines = user.summary.split('\n')
        edit_boxes, summary_box_count = getSummaryEditHtml(summary_lines)
    else:
        edit_boxes, summary_box_count = getSummaryEditHtml([])

    html =  '<input id="summaryInputLastIndex" name="summaryInputLastIndex" type="hidden" value="' + str(summary_box_count) + '" /> \n '
    html += '<div id="summary_edit_boxes">' + edit_boxes + '</div>\n '
    return html

def getJobPrefDisplay(user):
    pref_summary = ''
    #12 Lakhs, Large Companies only, in Bangalore.
    if user.pref_designation or user.min_salary or user.pref_location or user.pref_employment:
        pref_summary += (str(user.min_salary/100000) + ' Lakh(s)',  '<em class="warn">Salary(unspecified)</em>')[user.min_salary == 0] + ', '
        pref_summary += (user.pref_designation, '<em class="warn">Designation(unspecified)</em>')[user.pref_designation == ''] + ' '
        pref_summary += 'in ' + (html_options.getVerboseEmploymentType(user.pref_employment), '<em class="warn">Employment Type(unspecified)</em>')[user.pref_employment == '']
        if user.pref_location:
            if not user.pref_location == 'Anywhere':    pref_summary += ', ' + user.pref_location
        else:   pref_summary += ', <em class="warn">Location(unspecified).</em>'
    else:
        pref_summary = 'Preferences not set.'

    return pref_summary

def getJobPrefEdit(user):
    min_salary_select_html = html_options.getSalarySelectHtml('minSalary', user.min_salary)
    pref_location_select_html = html_options.getLocationSelectHtml('prefLocation', user.pref_location)
    pref_employment_select_html = html_options.getEmploymentSelectHtml('prefEmployment', user.pref_employment)

    html =  '<p>Minimum Expected Salary <br /> ' + min_salary_select_html + '</p>\n '
    html += '<p>Preferred Designation <br /> <input id="prefDesignation" name="prefDesignation" type="text" size="40" value="' + user.pref_designation + '" /></p>\n '
    html += '<p>Preferred Location <br /> ' + pref_location_select_html + '</p>\n '
    html += '<p>Preferred Employment <br /> ' + pref_employment_select_html + '</p>\n '
    return html

def getPersonalInfoDisplay(user):
    html =  '<span class="faded">Designation:</span> ' + (user.curr_designation, '<em class="warn">unspecified</em>')[user.curr_designation == ''] + '<br />'
    html += '<span class="faded">Employer type:</span> ' + (user.curr_employer, '<em class="warn">unspecified</em>')[user.curr_employer == ''] + '<br />'
    html += '<span class="faded">Experience:</span> ' + (str(user.experience), '<em class="warn">unspecified</em>')[user.experience == 0] + ' years<br />'
    html += '<span class="faded">Skills:</span> ' + (user.tags, '<em class="warn">unspecified</em>')[user.tags == ''] + '<br />'
    return html

def getPersonalInfoEdit(user):
    curr_employer_select_html = html_options.getEmployerSelectHtml('currEmployer', user.curr_employer)
    experience_select_html = html_options.getExperienceSelectHtml('experience', user.experience)
    html =  '<p>Current designation: <br /> <input id="curr_designation" name="curr_designation" type="text" size="40" value="' + user.curr_designation + '" /></p>\n'
    html += '<p>Current Employer: <br /> ' + curr_employer_select_html + '</p>\n'
    html += '<p>Experience in years: <br /> ' + experience_select_html + '</p>\n'
    html += '<p>Skills: <br /> <textarea name="tags" cols="64" rows="3" id="tags">' + user.tags  + '</textarea></p>\n'
    return html

def getJobInterestDisplay(user):
    return {'yes': 'Your resume is available to recruiters.',
            'no': 'Your <span class="warn">resume is hidden</span> from recruiters.'}[user.is_job_hunting]

def getSummaryEditHtml(summary_lines):
    numBoxes = lambda x: ((x/5)+1)*5
    summary_edit = ''
    box_count = numBoxes(len(summary_lines))
    for i in range(box_count):
        if i < len(summary_lines):
            summary_edit += '<div id="summaryInputContainer%d">\n<input type="text" class="summaryInput" size="64" value="%s" />' % (i+1, summary_lines[i])
            summary_edit += '<img src="/images/delete.gif" alt="clear" class="summaryRemoveImg" /><a href="javascript:removeBox(\'summaryInputContainer%d\');">clear</a></div>' % (i+1)
        else:
            summary_edit += '<div id="summaryInputContainer%d">\n<input type="text" class="summaryInput" size="64" value="" /><img src="/images/delete.gif" alt="clear" class="summaryRemoveImg"/><a href="javascript:removeBox(\'summaryInputContainer%d\');">clear</a></div>' % (i+1, i+1)

    return summary_edit, box_count

def getWeekName(date):
    from datetime import datetime, timedelta
    first_day_of_month = datetime(date.year, date.month, 1)
    first_day_of_next_month = (datetime(date.year, date.month+1, 1), datetime(date.year+1, 1, 1))[date.month == 12]
    last_day_of_month = first_day_of_next_month - timedelta(days=1)

    first_week_of_month = first_day_of_month.isocalendar()[1]
    current_week = date.isocalendar()[1]
    first_week_next_month = first_day_of_next_month.isocalendar()[1]

    if current_week < first_week_of_month:
        week_num, week_month, week_year  = current_week, date.strftime('%B'), date.year

    elif current_week == first_week_next_month:
        week_num, week_month, week_year  = 1, first_day_of_next_month.strftime('%B'), first_day_of_next_month.year

    else:
        week_num, week_month, week_year  = current_week - first_week_of_month + 1, date.strftime('%B'), date.year

    return "%s week, %s %d" %({1:'1st', 2:'2nd', 3:'3rd', 4:'4th', 5:'5th'}[week_num], week_month, week_year)

def getIsResumeVisibleSelectHtml(element_name, selection):
    is_jobhunting_options = [('Yes','yes'), ('No', 'no')]
    return hotmetal.elemSelect([], is_jobhunting_options, lambda x:x[0], lambda x:x[1], selection, 'name="' + element_name + '" id="' + element_name + '"')
