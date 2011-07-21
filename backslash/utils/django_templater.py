#!/usr/bin/env python
import os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):    os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
from django.template import Template, Context
from django.utils.encoding import smart_str

def render(template_html, dictionary):
    return smart_str(Template(template_html).render(Context(dictionary)))