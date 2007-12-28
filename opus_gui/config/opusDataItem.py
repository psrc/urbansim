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
    def __init__(self,domDocument, node, row, parent):
        self.domDocument = domDocument
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
                childItem = OpusDataItem(self.domDocument,childNode, i , self)
                self.childItems.append(childItem)
                i = i + 1
                childItem.initAsRootItem()

    def node(self):
        return self.domNode
    
    def parent(self):
        return self.parentItem
    
    def remove(self):
        # Need to remove the node...
        self.parentItem.domNode.removeChild(self.domNode)
        #self.parentItem.childItems.remove(self)
        indexSelf = self.parentItem.childItems.index(self)
        for x in xrange(indexSelf,len(self.parentItem.childItems)):
            print "X index = ", x
            self.parentItem.childItems[x].rowNumber = self.parentItem.childItems[x].rowNumber - 1
        print len(self.parentItem.childItems)
        self.parentItem.childItems.remove(self)
        print len(self.parentItem.childItems)
        
    def addChild(self,elementTag,elementType,elementText):
        # Need to add node to dom
        print "parent has %d child items" % (self.domNode.childNodes().count())
        newElement = self.domDocument.createElement(QString(elementTag))
        newElement.setAttribute(QString("type"),elementType)
        self.domNode.appendChild(newElement)
        if elementText != "":
            # Add a text Node
            newText = self.domDocument.createTextNode(QString(elementText))
            newElement.appendChild(newText)
        print "parent has %d child items" % (self.domNode.childNodes().count())
        # Then add the node to the model with a new item
        print "item has %d child items" % (len(self.childItems))
        childItem = OpusDataItem(self.domDocument, newElement,len(self.childItems),self)
        self.childItems.append(childItem)
        print "item has %d child items" % (len(self.childItems))
        
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
                childItem = OpusDataItem(self.domDocument,childNode, i , self)
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
    
