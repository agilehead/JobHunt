#!/usr/bin/env python
from django.db import models
from django.contrib import admin

from account import Account
from received_mail import ReceivedMail
from index_delta import IndexDelta

class User(models.Model):
    account = models.OneToOneField(Account, related_name='user')
    key = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)

    #general/current stuff - All lies
    is_job_hunting = models.CharField(max_length=20, default='yes')
    industry = models.CharField(max_length=100, blank=True, default='IT')
    experience = models.IntegerField(default=0)
    curr_employer = models.CharField(max_length=100, blank=True, default='')
    curr_designation = models.CharField(max_length=100, blank=True, default='')
    tags = models.TextField(blank=True, default='')
    summary = models.TextField(blank=True, default='')
    settings_edited = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    #desired - sweet dreams
    min_salary = models.IntegerField(default=0)
    pref_employment = models.CharField(max_length=100, blank=True, default='')
    pref_designation = models.CharField(max_length=100, blank=True, default='')
    pref_location = models.CharField(max_length=100, blank=True, default='')

    #files - the money
    doc_filename = models.CharField(max_length=100, blank=True, default='')
    doc_filepath = models.CharField(max_length=100, blank=True, default='')
    html_filepath = models.CharField(max_length=100, blank=True, default='')
    text_filepath = models.CharField(max_length=100, blank=True, default='')

    #for our eyes only...
    proxy_email = models.CharField(max_length=100, blank=True, default='')
    mail_ref = models.ForeignKey(ReceivedMail, null=True, blank=True)
    tagged = models.BooleanField(default=False)
    tagged_on = models.DateTimeField(null=True, blank=True)
    resume_updated_on = models.DateTimeField(null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, username, password, account_type, key, name='', email='', telephone='', doc_filename='', doc_filepath='', proxy_email='', resume_updated_on=None):
        account = Account.create(username, password, account_type)
        user = User()
        #account=account, name=name, email=email, telephone=telephone, doc_filename=doc_filename, doc_filepath=doc_filepath)
        user.account = account
        user.key = key
        user.email = email
        user.name = name
        user.telephone = telephone

        user.doc_filename = doc_filename
        user.doc_filepath = doc_filepath
        user.proxy_email = proxy_email
        user.resume_updated_on = resume_updated_on

        user.save()
        return user

    def delete(self):
        IndexDelta(user_id=self.id, index_type='D').save()
        import os, shutil
        if self.doc_filepath and os.path.exists(self.doc_filepath):
            dirname = os.path.dirname(self.doc_filepath).split('/')[-1]
            dumpyard_path = '/apps/jobhuntin/data/deleted'
            if not os.path.exists(dumpyard_path + '/' + dirname):   os.mkdir(dumpyard_path + '/' + dirname)
            if not os.path.exists(dumpyard_path + '/' + dirname + '/' + self.key):   os.mkdir(dumpyard_path + '/' + dirname + '/' + self.key)
            shutil.move(self.doc_filepath, dumpyard_path + '/' + dirname + '/' + self.key + '/' + self.doc_filename)

            #cleanup - remove html and text files if exists
            try:
                if os.path.exists(self.html_filepath):  os.remove(self.html_filepath)
                if os.path.exists(self.text_filepath):  os.remove(self.text_filepath)
            except:
                pass
        super(User, self).delete()

    def save(self):
        import sys, datetime
        sys.path.append('/websites/jobhuntin')
        from utils import mailer, eventnotifier
        if not self.id:
            eventnotifier.sendEventNotification('New User: %s posted on: %s' % (self.doc_filename, datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S %p')))

        if self.name and self.email and self.tags and self.pref_location:
            if not self.tagged:
                self.tagged = True
                from datetime import datetime
                self.tagged_on = datetime.utcnow()

        if self.account.account_type == 'FU' and self.id > 0 and self.tagged:
            user_old = User.objects.get(id=self.id)
            if user_old and not user_old.email:
                params = {'user_key': self.key }
                usrs = User.objects.filter(email=self.email, account__account_state='A', id__lt=self.id)
                if usrs:
                    if usrs.filter(account__account_type = 'PU'):
                        mailer.sendPremiumUserLoginToUpdateAlert(self.email, by_mail = bool(self.mail_ref))
                        self.delete()
                        return
                    else:
                        for usr in usrs.all():
                            usr.account.account_state = 'I'
                            usr.account.save()
                            IndexDelta(user_id=usr.id, index_type='D').save()

                        mailer.sendResumeUpdatedMail(self.email, params)
                else:
                    mailer.sendResumeAddedMail(self.email, params)

        super(User, self).save()
        
        #If he is tagged and is job hunting, he has to be indexed
        if self.tagged and self.is_job_hunting == 'yes':    IndexDelta(user_id=self.id, index_type='U').save()

    def __unicode__(self):
        if self.account.account_type == 'FU':
            if not self.html_filepath:
                return u'Html not converted:%s posted on: %s' % (self.doc_filename, self.posted_on.strftime('%d/%m/%Y %H:%M:%S %p'))
            elif not self.tagged:
                if self.email:
                    return u'Parsed, Not tagged:%s posted on: %s' % (self.doc_filename, self.posted_on.strftime('%d/%m/%Y %H:%M:%S %p'))
                else:
                    return u'Not tagged:%s posted on: %s' % (self.doc_filename, self.posted_on.strftime('%d/%m/%Y %H:%M:%S %p'))
            else:
                return u'%s with %d years in %s' % (self.tags, self.experience, self.pref_location)
        
        elif self.account.account_type == 'PU':
            return u'Premium User:%s' % (self.name)
        
    class Meta:
        app_label = 'website'


class UserAdmin(admin.ModelAdmin):
    change_form_template = 'sys/user_change_form.html'

admin.site.register(User, UserAdmin)
