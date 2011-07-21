from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.template.context import RequestContext
from utils import dataplus
from  website import codejar

def createItem(name, description, val, subCategories = None, addlParams = None):
    dict = {'name':name, 'description':description, 'value':val, 'subCategories':subCategories }
    if addlParams:
        for k,v in addlParams.iteritems():  dict[k] = v
    return dict    

def createItems(list, default = None):    
    result = {}
    result['items'] = []
    for item in list:
        if len(item) == 5:
            result['items'].append(createItem(item[0], item[1], item[2], item[3], item[4]))
        elif len(item) == 4:
            result['items'].append(createItem(item[0], item[1], item[2], item[3]))
        else:
            result['items'].append(createItem(item[0], item[1], item[2]))
    result['default'] = default
    return result

themes = createItems(
    [('Blue', None, 'blue', None, {'rating':3}),
    ('Classic', None, 'classic', None, {'rating':3}),
    ('Crystal', None, 'crystal', None, {'rating':4}),
    ('Desert', None, 'desert', None, {'rating':4}),
    ('Eighties', None, 'eighties', None, {'rating':4}),
    ('Elegant', None, 'elegant', None, {'rating':5}),
    ('Fancy', None, 'fancy', None, {'rating':5}),
    ('Formal', None, 'formal', None, {'rating':5}),
    ('Green', None, 'green', None, {'rating':4}),
    ('Moderna', None, 'moderna', None, {'rating':4}),
    ('Ruby', None, 'ruby', None, {'rating':5}),
    ('Simple', None, 'simple', None, {'rating':4})], 'moderna')
    
style_chrono = ('Chronological', 'Chronological is the most common resume format used worldwide, elegantly highlighting the career path of the candidate.', 'chronological', themes)
style_functional = ('Functional', 'Functional Style Resumes focus on Skills and Projects, instead of Employment History.', 'functional', themes)
style_combination = ('Combination', 'This is a combination of Chronological and Functional styles.', 'combination', themes)
style_alternate = ('Alternate', 'An interesting variation', 'structured', themes)

common_formats = createItems([style_chrono, style_functional, style_combination], 'chronological')
all_formats = createItems([style_chrono, style_functional, style_combination, style_alternate], 'chronological')
chrono_only = createItems([style_chrono], 'chronological')

it_profiles = createItems(
    [('Developer', None, 'dev', all_formats),
    ('Tester', None, 'tester', all_formats),
    ('Architect', None, 'architect', all_formats),
    ('Consultant', None, 'consultant', chrono_only),
    ('DBA', None, 'dba', chrono_only),
    ('Project Manager', None, 'projectmgr', common_formats),
    ('System Administrator', None, 'sysadmin', chrono_only),
    ('HR Executive', None, 'hrexec', common_formats),
    ('HR Manager', None, 'hrmgr', common_formats),
    ('Pre Sales', None, 'presales', chrono_only),
    ('Business Development', None, 'bdm', chrono_only),
    ('Business Analyst', None, 'ba', chrono_only)], 'dev')
    
#manager_profiles = createItems(
#    [('Project Manager', None, 'project_manager', common_formats),
#    ('Vice President', None, 'vp', common_formats)], 'vp')

industries = createItems(
    [('IT/Computing', None, 'it', it_profiles)], 'it')

def handle(request):
    if request.method in ['GET','HEAD']:
        role = dataplus.dictGetSafeVal(request.REQUEST, 'role', '')
        if role and role.find('_') > 0:
            role_parts = role.split('_')
            role_list = findSubFromList(industries, role_parts[0])
            if role_list:
                industries['default'] = role_parts[0]
                if findSubFromList(role_list, role_parts[1]):
                    role_list['default'] = role_parts[1]
        
        context=RequestContext(request)
        context.autoescape = False
        return codejar.actions.render(request, 'gallery/index.htm',
            {'categorization': simplejson.dumps(industries)}, context)

def findSubFromList(dict, name):
    for item in dict['items']:
        if name == item['value']:  return item['subCategories']
