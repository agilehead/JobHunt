from django.template import TemplateDoesNotExist
from django.http import Http404
from website import codejar

def handle(request, url):
    try:
        return codejar.actions.render(request, url)
    except TemplateDoesNotExist:
        raise Http404