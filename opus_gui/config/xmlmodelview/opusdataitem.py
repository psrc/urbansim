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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtXml import *


class OpusDataItem:
    def __init__(self,domDocument, node, row, parentOpusDataItem):
        self.domDocument = domDocument
        self.domNode = node
        self.parentOpusDataItem = parentOpusDataItem
        self.childItems = []

    def initAsRootItem(self):
        i = 0
        for x in xrange(0,self.domNode.childNodes().count(),1):
            current = self.domNode.childNodes().item(x)
            if (current.attributes().namedItem(QString("flags")).isNull() or \
                current.attributes().namedItem(QString("flags")).nodeValue() != QString("hidden")) and \
                (current.nodeType() == QDomNode.ElementNode):
                childNode = self.domNode.childNodes().item(x)
                childItem = OpusDataItem(self.domDocument,childNode, i , self)
                self.childItems.append(childItem)
                i = i + 1
                childItem.initAsRootItem()

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentOpusDataItem

    def child(self,i):
        #print "DataItem.child ", i
        if len(self.childItems) > i:
            return self.childItems[i]
        tryToFind = i+1
        foundSoFar = 0
        for x in xrange(0,self.domNode.childNodes().count(),1):
            current = self.domNode.childNodes().item(x)
            if (current.attributes().namedItem(QString("flags")).isNull() or \
                current.attributes().namedItem(QString("flags")).nodeValue() != QString("hidden")) and \
                (current.nodeType() == QDomNode.ElementNode):
                # We found one
                foundSoFar = foundSoFar + 1
            if foundSoFar == tryToFind:
                # We have the one we are looking for
                childNode = self.domNode.childNodes().item(x)
                childItem = OpusDataItem(self.domDocument,childNode, i , self)
                self.childItems.append(childItem)
                return childItem
        return None

    def row(self):
        return self.parentOpusDataItem.childItems.index(self)

    def numChildren(self):
        return len(self.childItems)

    def lastChild(self):
        if len(self.childItems) > 0:
            return self.childItems[-1]
        else:
            return None
