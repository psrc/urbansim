#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

'''

Things to watch out for,
check that 'christofferklang' is not in the tree (from OPUS_HOME)

'''

from xml.etree.cElementTree import *

def typestring(obj):
    ''' Returns a string that represent the type for a given object '''
    type_str = ''
    if isinstance(obj, str):
        # if the string starts with a quote, assume it's a quoted string
        if obj.startswith('"') or obj.startswith("'"):
            type_str = 'quoted_string'
        else:
            type_str = "string"

    elif isinstance(obj, int):
        type_str = "integer"
    elif isinstance(obj, list):
        type_str = "list"
    elif isinstance(obj, dict):
        type_str = "dictionary"
    return type_str

def dict_to_node(parent_node, d):
    for key, value in d.items():
        arguments = {'type': typestring(value)}
        node = SubElement(parent_node, str(key), arguments)
        if isinstance(value, dict):
            dict_to_node(node, value)
        else:
            node.text = str(value)

        #if isinstance(d[key], dict):
        #    dict_to_node(node, d[key])
        #else:
        #    node.text = str(d[key])

def show_tree(root):
    _indent(root)
    f = open('/Users/christofferklang/Documents/workspace/tmp/dict_to_xml.xml', 'w')
    f.write(tostring(root))

def _indent(element, level=0):
    '''
    Indents the (internal) text representation for an Element.
    This is used before saving to disk to generate nicer looking XML files.
    (this code is based on code from http://effbot.org/zone/element-lib.htm)
    '''
    i = "\n" + level * "  "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = i + "  "
        if not element.tail or not element.tail.strip():
            element.tail = i
        child_element = None
        for child_element in element:
            _indent(child_element, level+1)
        if not child_element.tail or not child_element.tail.strip():
            child_element.tail = i
    else:
        if level and (not element.tail or not element.tail.strip()):
            element.tail = i

