#!/usr/bin/env python

flash_messages = {'upload_file_not_found': 'Please select the resume to upload.',
            'unsupported_doctype_upload': 'Invalid file type. Please upload resume in Microsoft Word format.',
            'large_doc_upload':'Please upload a smaller file. Maximum allowed size is 1MB.',
            'unknown':'We are having a technical issue. Please upload after sometime.',
            'login_failed':'Invalid username/password. Please try again.',
            'activation_pending':'Please check your email and click on the activation link to activate your account.',
            'resume_uploaded':'Your resume has been uploaded.',
            'profile_updated':'Your profile settings have been updated.',
            'logged_out':'You logged out.',
            'not_logged_in':'You are not logged in.',
            'password_changed': 'Your password has been updated.',
            'pwd_change_emailed': 'A link to reset your password has been emailed to you.',
            'malformed_url': 'This url is malformed, please use the link in the email that was sent to you.',
            'welcome_user': 'Congratulations! You have created a new account.',
            'recruiters_invited': 'Recruiters have been invited.',
            'email_sent': 'The email has been sent successfully.',
            }

def getFlashMessage(flash_id):
    if flash_messages.has_key(flash_id):
        return flash_messages[flash_id]
    else:
        return ''
