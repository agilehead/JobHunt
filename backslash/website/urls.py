from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Views:
    (r'(?i)^$', 'website.views.index.handle'),
    (r'(?i)^index\.htm$', 'website.views.index.handle'),
    (r'(?i)^resumeactive\.htm$', 'website.views.resumeactive.handle'),
    (r'(?i)^jobpref\.htm$', 'website.views.jobpref.handle'),#link from mail
    (r'(?i)^tellfriends\.htm$', 'website.views.tellfriends.handle'),
    (r'(?i)^msg\.htm$', 'website.views.msg.handle'),
    (r'(?i)^removeresume\.htm$', 'website.views.removeresume.handle'),
    
    (r'(?i)^login\.htm$', 'website.views.login.handle'),
    (r'(?i)^logout\.htm$', 'website.views.logout.handle'),
    (r'(?i)^forgotpassword\.htm$', 'website.views.forgotpassword.handle'),
    
    #Anon Users
    (r'(?i)^signup\.htm$', 'website.views.signup.handle'),
    (r'(?i)^dashboard\.htm$', 'website.views.dashboard.handle'),
    (r'(?i)^changepassword\.htm$', 'website.views.changepassword.handle'),
    (r'(?i)^viewresume\.htm$', 'website.views.viewresume.handle'),
    (r'(?i)^uploadresume\.htm$', 'website.views.uploadresume.handle'),
    (r'(?i)^changepassword\.htm$', 'website.views.changepassword.handle'),
    (r'(?i)^viewsummary\.htm$', 'website.views.viewsummary.handle'),
    (r'(?i)^resumesentreport\.htm$', 'website.views.resumesentreport.handle'),
    (r'(?i)^paymentsuccess\.htm$', 'website.views.paymentsuccess.handle'),
    
    
    #Recruiters
    (r'(?i)^recruiters/?$', 'website.views.recruiters_index.handle'),
    (r'(?i)^recruiters/dashboard\.htm$', 'website.views.recruiters_dashboard.handle'),
    (r'(?i)^recruiters/subscribe\.htm$', 'website.views.recruiters_subscribe.handle'),
    (r'(?i)^recruiters/subscriptions\.htm$', 'website.views.recruiters_subscriptions.handle'),
    (r'(?i)^recruiters/signup\.htm$', 'website.views.recruiters_signup.handle'),
    (r'(?i)^recruiters/searchresults\.htm$', 'website.views.recruiters_searchresults.handle'),    
    (r'(?i)^recruiters/settings\.htm$', 'website.views.recruiters_settings.handle'),
    (r'(?i)^(?P<account_type>\w+)/changepassword\.htm$', 'website.views.changepassword.handle'),
    (r'(?i)^recruiters/emailverified\.htm$', 'website.views.recruiters_emailverified.handle'),
    (r'(?i)^(?P<account_type>recruiter)s/viewresumesummary\.htm$', 'website.views.viewsummary.handle'),
    (r'(?i)^recruiters/invites\.htm$', 'website.views.recruiters_invites.handle'),
    (r'(?i)^recruiters/emailusers\.htm$', 'website.views.recruiters_emailusers.handle'),
    (r'(?i)^recruiters/propactivation\.htm$', 'website.views.recruiters_propactivation.handle'),
    
    # Sys
    (r'(?i)^sys/resumes/(?P<format>\w+)/(?P<user_id>\d+)/?$', 'website.views.sys_viewresume.handle'),
    (r'(?i)^sys/searchresumes\.htm$', 'website.views.sys_searchresumes.handle'),
    (r'(?i)^sys/recinvite\.htm$', 'website.views.sys_recinvite.handle'),
    
    #Resumes
    (r'(?i)^resumes/(?P<format>\w+)/(?P<user_key>\w+)/?$', 'website.views.recruiters_downloadresume.handle'),
    (r'(?i)^res/(?P<user_key>\w+)', 'website.views.recruiters_downloaddocresume.handle'),
    
     # Gallery
    (r'(?i)^gallery/$', 'website.views.gallery_index.handle'),
    (r'(?i)^gallery/index.htm$', 'website.views.gallery_index.handle'),
    
    # Ajax calls
    (r'(?i)^ajax/recruiters/deletefilter\.ajax$', 'website.ajax.recruiters_deletefilter.handle'),
    (r'(?i)^ajax/recruiters/requestresume\.ajax$', 'website.ajax.recruiters_requestresume.handle'),
    (r'(?i)^ajax/updateprofile\.ajax$', 'website.ajax.updateprofile.handle'),
    (r'(?i)^ajax/sendactivationemail\.ajax$', 'website.ajax.sendactivationemail.handle'),
    (r'(?i)^ajax/signup\.ajax$', 'website.ajax.signup.handle'),
    
    #Generic html page handler
    (r'(?i)^(?P<url>.+\.html)$', 'website.views.generic.handle'),

    # Uncomment this for admin:
    (r'^admin/(.*)', admin.site.root),
)
