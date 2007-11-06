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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtXml import *


class OpusDataItem:
    def __init__(self,node, row, parent):
        self.domNode = node
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = []
    
    #def initAsRootItem(self):
    #    if self.domNode.childNodes().count() == 1:
    #        current = self.domNode.childNodes().item(0)
    #        childItem = OpusDataItem(current, 0 , self)
    #        self.childItems.append(childItem)
    #        self.initAsRootChild()
    #    else:
    #        print "ERROR - XML has more than one root configuration item"

    def initAsRootItem(self):
        i = 0
        for x in xrange(0,self.domNode.childNodes().count(),1):
            current = self.domNode.childNodes().item(x)
            if (current.attributes().namedItem(QString("flags")).isNull() or \
                current.attributes().namedItem(QString("flags")).nodeValue() != QString("hidden")) and \
                (current.nodeType() == QDomNode.ElementNode):
                childNode = self.domNode.childNodes().item(x)
                childItem = OpusDataItem(childNode, i , self)
                self.childItems.append(childItem)
                i = i + 1
                childItem.initAsRootItem()

    def node(self):
        return self.domNode
    
    def parent(self):
        return self.parentItem
    
    def child(self,i):
        #print "DataItem.child ", i
        if len(self.childItems) > i:
            return self.childItems[i]
        tryToFind = i+1
        foundSoFar = 0
        for x in xrange(0,self.domNode.childNodes().count(),1):
            current = self.domNode.childNodes().item(x)
            if (current.attributes().namedItem(QString("flags")).isNull() or \
                current.attributes().namedItem(QString("flags")).nodeValue() != QString("OpusHidden")) and \
                (current.nodeType() == QDomNode.ElementNode):
                # We found one
                foundSoFar = foundSoFar + 1
            if foundSoFar == tryToFind:
                # We have the one we are looking for
                childNode = self.domNode.childNodes().item(x)
                childItem = OpusDataItem(childNode, i , self)
                self.childItems.append(childItem)
                return childItem
        return None
        #if i>=0 and i<self.domNode.childNodes().count():
        #    childNode = self.domNode.childNodes().item(i)
        #    childItem = OpusDataItem(childNode, i , self)
        #    self.childItems.append(childItem)
        #    return childItem
        #return 0
    
    def row(self):
        return self.rowNumber
    
