from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from utils import dataplus
from website import models, codejar

def handle(request):
    user_key = dataplus.dictGetSafeVal(request.REQUEST, 'key', '')
    user = dataplus.returnIfExists(models.User.objects.filter(key=user_key, account__account_type='FU'))
    if not user:
        return codejar.actions.render(request, 'info.htm', {'info_header':'Resume not found',
                                                            'info_text':'This resume does not exist,<br /> or may have been deleted.'})
    
    if request.method == 'GET':
        return codejar.actions.render(request, 'removeresume.htm', {'user_key':user_key})
    elif request.method == 'POST':
        user.delete()
        return codejar.actions.render(request, 'info.htm', {'info_header':'Your resume has been removed',
                                                            'info_text':"""<p>To make your resume active again, just <a href="/">upload it</a><br />
                                                                            or send it as an attachment to <a href="mailto:post@jobhunt.in">post@jobhunt.in</a>.</p>
                                                                            <p>Thank you.</p>"""})
        