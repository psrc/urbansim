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
from PyQt4.QtCore import QString

class XmlItem(object):
    def __init__(self, domDocument, node, parentOpusDataItem):
        self.domDocument = domDocument
        self.domNode = node
        self.parentOpusDataItem = parentOpusDataItem
        self.childItems = []

    def initAsRootItem(self):
        '''use this element as a root item and selectively add its children'''
        for x in xrange(0, self.domNode.childNodes().count(), 1):
            child_node = self.domNode.childNodes().item(x).toElement()
            # do not add nodes (or subtrees) that should be hidden
            if not child_node.isNull() and \
                child_node.attribute('hidden').toLower() != QString('true'):
                child_item = XmlItem(self.domDocument, child_node, self)
                self.childItems.append(child_item)
                # descend into childs subtree
                child_item.initAsRootItem()

    def refresh(self):
        '''refreshes this item and all of it's children'''
        self.childItems = []
        self.initAsRootItem()

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentOpusDataItem

    def child(self, i):
        #print "DataItem.child ", i
        if len(self.childItems) > i:
            return self.childItems[i]
        tryToFind = i+1
        foundSoFar = 0
        for x in xrange(0, self.domNode.childNodes().count(), 1):
            current = self.domNode.childNodes().item(x)
            if current.isElement() and not \
                current.toElement().attribute('hidden').toLower() == QString('true'):
                # We found one
                foundSoFar = foundSoFar + 1
            if foundSoFar == tryToFind:
                # We have the one we are looking for
                childNode = self.domNode.childNodes().item(x)
                childItem = XmlItem(self.domDocument, childNode, i , self)
                self.childItems.append(childItem)
                return childItem
        return None

    def row(self):
        if self.parentOpusDataItem:
            try:
                index = self.parentOpusDataItem.childItems.index(self)
            except:
                index = 0
            return index
        else:
            return 0

    def numChildren(self):
        return len(self.childItems)

    def lastChild(self):
        if len(self.childItems) > 0:
            return self.childItems[-1]
        else:
            return None
