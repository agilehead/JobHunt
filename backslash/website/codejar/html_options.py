from utils import hotmetal

locations = ['Bangalore', 'Chennai', 'Hyderabad', 'Delhi,Noida,NCR', 'Kolkata', 'Pune', 'Mumbai', '-', 'Anywhere', '-',
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
            'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra',
            'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', '-',
            'Anywhere in North India', 'Anywhere in South India', 'Anywhere in East India', 'Anywhere in West India']

salary_levels = [100000, 200000, 300000, 400000, 500000, 600000, 800000, 1000000,
                1200000, 1400000, 1600000, 2000000, 2400000, 3000000]

employment_types = [('Only Large Companies/MNCs', 'Large Companies or MNCs'),
                ('Only Consulting Roles', 'Consulting'),
                ('Only Part-time Jobs', 'Part-time'),
                ('Only Jobs outside India', 'Abroad')]

employer_types = [('Large Company/MNC', 'Large Company or MNC'),
                ('Medium Sized Company', 'Medium Sized Company'),
                ('Small Company/Startup', 'Small Company or Startup'),
                ('Self Employed/Consulting', 'Self Employed or Consulting')]

def getExperienceSelectHtml(element_name, selection):
    return hotmetal.elemSelect([('Select','Select')], range(0,21), lambda x:str(x), lambda x:str(x), selection, 'name="' + element_name + '" id="' + element_name + '"')

def getSalarySelectHtml(element_name, selection):
    return hotmetal.elemSelect([('Select','Select')], salary_levels, lambda x:str(x/100000) + ' Lakhs', lambda x:str(x), selection, 'name="' + element_name + '" id="' + element_name + '"')

def getLocationSelectHtml(element_name, selection):
    trimLocation = lambda x: (x, x[len('Anywhere in '):])[x.startswith('Anywhere in ')]
    return hotmetal.elemSelect([('Select','Select')], locations, lambda x:x, trimLocation, selection, 'name="' + element_name + '" id="' + element_name + '"')

def getEmploymentSelectHtml(element_name, selection):
    return hotmetal.elemSelect([('Select','Select')], employment_types, lambda x:x[0], lambda x:x[1], selection, 'name="' + element_name + '" id="' + element_name + '"')

def getEmployerSelectHtml(element_name, selection):
    return hotmetal.elemSelect([('Select','Select')], employer_types, lambda x:x[0], lambda x:x[1], selection, 'name="' + element_name + '" id="' + element_name + '"')

def getVerboseEmploymentType(value):
    for option in employment_types:
        if option[1] == value:  return option[0]
    return value

def getVerboseEmployerType(value):
    for option in employer_types:
        if option[1] == value:  return option[0]
    return value
