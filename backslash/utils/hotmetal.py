#!/usr/bin/env python
#HTML helper (HoTMetaL)
import cgi

def elemSelect(defaults, options, text_selector, value_selector, selected_value, attributes):
    selected_value = str(selected_value)
    attributes = ' ' + attributes
    selection_done = False
    elemSelect = '<select' + attributes + '>\r\n'
    for val in defaults:
        if (not selection_done and selected_value == val[1]):
            elemSelect += '\t<option value="' + cgi.escape(val[1])  + '" selected="selected">' + cgi.escape(val[0]) + '</option>'
            selection_done = True
        else:            
            elemSelect += '\t<option value="' + cgi.escape(val[1])  + '">' + cgi.escape(val[0]) + '</option>'
            
    for val in options:
        text = str(text_selector(val))
        value = str(value_selector(val))
        if (not selection_done and selected_value == value):
            elemSelect += '\t<option value="' + cgi.escape(value)  + '" selected="selected">' + cgi.escape(text) + '</option>'
            selection_done = True
        else:
            elemSelect += '\t<option value="' + cgi.escape(value) + '">' + cgi.escape(text) + '</option>'    
    elemSelect += '</select>\r\n'
    
    return elemSelect