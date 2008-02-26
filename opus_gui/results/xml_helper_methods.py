# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from PyQt4.QtCore import QString

def elementsByAttributeValue(domDocument,
                             attribute,
                             value):
                             #parent_name = None):
    first_child = domDocument.documentElement() 
    matches = []
    _elementsByAttributeValue(first_child = first_child, 
                               domDocument = domDocument, 
                               attribute = QString(attribute), 
                               value = QString(value),
                               matches = matches)

    return matches
       
def _elementsByAttributeValue(first_child,
                              domDocument,
                              attribute,
                              value,
                              matches):

    node = first_child  
    while not node.isNull():
        if node.isElement():
            domElement = node.toElement()
            if domElement.isNull():
                continue

            if domElement.attribute(attribute) == value:
                matches.append((domElement,node))
            
        if node.hasChildNodes():
            first_child = node.firstChild()
            _elementsByAttributeValue(
                   first_child = first_child, 
                   domDocument = domDocument, 
                   attribute = attribute, 
                   value = value, 
                   matches = matches)
        node = node.nextSibling()
            
def get_child_values(parent, child_names):
    child_vals = {}
    node = parent.firstChild()
    while not node.isNull():
        if node.nodeName() in child_names:
            if node.isElement():
                domElement = node.toElement()
                child_vals[str(node.nodeName())] = domElement.text()
        node = node.nextSibling()
    return child_vals
