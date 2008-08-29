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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
       
class DatabaseSettingsDataView(QTreeView):
    def __init__(self, mainwindow):
        QTreeView.__init__(self, mainwindow)
        self.mainwindow = mainwindow
        self.qdoc = QDomDocument()
        

    def openDefaultItems(self):
        # Loop through all the data model items displayed and expand
        # if they are marked to be expanded by default
        model = self.model()
        self.loopItems(model,model.index(0,0,QModelIndex()).parent())

    def loopItems(self,model,parentIndex):
        rows = model.rowCount(parentIndex)
        for x in xrange(0,rows,1):
            child = model.index(x,0,parentIndex)
            childElement = child.internalPointer().domNode.toElement()
            #expand each of the first level of children under the root.
            if not childElement.isNull():
                self.expand(child)

   
class DatabaseSettingsDataModel(QAbstractItemModel):
    def __init__(self, document, mainwindow, configFile, xmlType, editable):
        QAbstractItemModel.__init__(self, mainwindow)
        #self.parentTree = parentTree
        self.mainwindow = mainwindow
        self.editable = editable
        self.configFile = configFile
        self.domDocument = document
        self.xmlType = "database_configurations"
        # Dirty flag for keeping track of edits...
        self.dirty = False
        
        # Root data for use in column headers
        self.rootData = []
        self.rootData.append(QVariant("Name"))
        #self.rootData.append(QVariant("Type"))
        self.rootData.append(QVariant("Value"))

        # Get the XML config data
        self.xmlRoot = document.elementsByTagName(QString(self.xmlType)).item(0)
        #print "Searching for ", self.xmlType
        if self.xmlRoot == None:
            print "No XML elements in the root with type ", self.xmlType
            return
        
        print "Found ", self.xmlRoot.nodeName()
        #self._rootItem = SettingsDataItem(document,document.documentElement(), 0, self)
        self._rootItem = SettingsDataItem(document,self.xmlRoot, 0, self)
        # Loop through the first level children and inti them as a root item
        # and append to the tree...
        for x in xrange(0,self.xmlRoot.childNodes().count(),1):
            current = self.xmlRoot.childNodes().item(x)
            self._rootItemSub = SettingsDataItem(document,current, x, self._rootItem)
            self._rootItemSub.initAsRootItem()
            self._rootItem.childItems.append(self._rootItemSub)

            
    def findXMLRoot(self,doc,tp):
        i = 0
        childNode = None
        for x in xrange(0,doc.childNodes().count(),1):
            current = doc.childNodes().item(x)
            if (current.attributes().namedItem(QString("type")).nodeValue() == QString(tp)) and \
                   (current.nodeType() == QDomNode.ElementNode):
                childNode = current
        return childNode

    
    # We only allow for one child colum per branch in the tree
    def columnCount(self, parent):
        #return 1
        return 2

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        if domNode.isNull():
            return QVariant()
        # Handle ElementNodes
        if domNode.isElement():
            domElement = domNode.toElement()
            if domElement.isNull():
                return QVariant()
            if index.column() == 0:
                if role == Qt.DecorationRole:
                    #return QVariant(self.database)
                    return QVariant()
                elif role == Qt.DisplayRole:
                    return QVariant(domElement.tagName())
                elif role == Qt.BackgroundRole:
                    if domElement.hasAttribute(QString("temporary")) and \
                           domElement.attribute(QString("temporary")) == QString("True"):
                        return QVariant(QColor(Qt.cyan))
                    else:
                        return QVariant(QColor(Qt.white))
                else:
                    return QVariant()
            #elif index.column() == 1:
            #    if role == Qt.DecorationRole:
            #        return QVariant()
            #    elif role == Qt.DisplayRole:
            #        return QVariant(domElement.attribute(QString("type")))
            #    else:
            #        return QVariant()
            elif index.column() == 1:
                if role == Qt.DecorationRole:
                    return QVariant()
                elif role == Qt.DisplayRole:
                    if domNode.hasChildNodes():
                        children = domNode.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                return QVariant(children.item(x).nodeValue())
                        return QVariant()
                    else:
                        return QVariant()
                else:
                    return QVariant()
            else:
                #We have a problem... should only be 2 columns
                print "Wrong number of columns"
                return QVariant()
        elif domNode.isComment():
            #show nothing, it is a comment
            return QVariant()
            
        else:
            print "Node is not handled yet in the DatabaseSettingsDataModel - ", str(domNode.nodeType())
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if self.editable == True:
            element = index.internalPointer().domNode.toElement()

            if index.column() == 0:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable                
            elif index.column() == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def headerData(self, section, oreientation, role):
        if oreientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.rootData[section])
        else:
            return QVariant()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        parentItem = None
        if not parent.isValid():
            # We start by setting the parent item to the _root
            #print "index non-valid root item row=%s column=%s" % (row,column)
            parentItem = self._rootItem
        else:
            # Else we just grab the Item that is the parent
            parentItem = parent.internalPointer()
        # Grab the child at the row passed in...
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        childItem = child.internalPointer()
        parentItem = childItem.parent()
        if not parentItem or parentItem == self._rootItem:
            return QModelIndex()
        #if parentItem == self._rootItem:
        #    return self.createIndex(0,0,parentItem)
        return self.createIndex(parentItem.row(),0,parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        parentItem = None
        if not parent.isValid():
            #print "row_count non-valid root item"
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        return len(parentItem.childItems)

    def markAsDirty(self):
        self.dirty = True

    def markAsClean(self):
        self.dirty = False
        
    def isDirty(self):
        return self.dirty
    
    def isTemporary(self,node):
        nodeElement = node.toElement()
        if not nodeElement.isNull():
            if nodeElement.hasAttribute(QString("temporary")):
                if nodeElement.attribute(QString("temporary")) == QString("True"):
                    return True
                else:
                    return False
        return False
        
    def checkIfInheritedAndAddBackToTree(self,nodePath,parentIndex):
        indentSize = 2
        print self.doDocument.toString(indentSize)
        #print "Checking if inherited: %s" % (nodePath) 
#        opusXMLTree = self.parentTree.toolboxbase.opusXMLTree
#        indentSize = 2
#        opusXMLTree.update(str(self.domDocument.toString(indentSize)))
#        found = opusXMLTree.find(str(nodePath))
#        if found is not None:
#            # Insert the inherited node
#            doc = QDomDocument()
#            doc.setContent(QString(found))
#            node = doc.firstChild()
#            if (node.isElement()) and \
#               (node.toElement().hasAttribute(QString("inherited"))):
#                self.insertRow(self.rowCount(parentIndex),parentIndex,node,False)

    def domNodePath(self,parent):
        prepend = ''
        parentElement = parent.toElement()
        if not parentElement.isNull():
            grandParent = parent.parentNode()
            if (not grandParent.isNull()) and \
               (grandParent.isElement()) and \
               (grandParent.toElement().tagName() != QString("opus_project")):
                prepend = self.domNodePath(grandParent)
            else:
                return parentElement.tagName()
            if prepend:
                return prepend + '/' + parentElement.tagName()
            else:
                return parentElement.tagName()
        return ''

    def validateTagName(self,tag):
        regex = QRegExp("[a-zA-Z_:][-a-zA-Z0-9._:]*")
        return regex.exactMatch(tag)

    def setData(self,index,value,role):
        if not index.isValid():
            return False
        if role != Qt.EditRole:
            return False
        #print "ModelView setData %s" % (value.toString())
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        if index.column() == 0:
            if domNode.isElement() and self.validateTagName(value.toString()):
                domElement = domNode.toElement()
                if not domElement.isNull():
                    # Check if the value has changed... only update if there is a change
                    # print "Original - " + domElement.tagName()
                    # print "New - " + value.toString()
                    if domElement.tagName() != value.toString():
                        domNodePath = self.domNodePath(domNode)
                        domElement.setTagName(value.toString())
                        if not self.isTemporary(domElement):
                            self.markAsDirty()
                            # Now check if it was inherited and the original should
                            # be added back in
                            self.checkIfInheritedAndAddBackToTree(domNodePath, index.parent())
            else:
                QMessageBox.warning(self.mainwindow,"Warning","Invalid Tag Name for XML Node... Please try again")
        elif index.column() == 1:
            if domNode.hasChildNodes():
                children = domNode.childNodes()
                for x in xrange(0,children.count(),1):
                    if children.item(x).isText():
                        if children.item(x).nodeValue() != value.toString():
                            children.item(x).setNodeValue(QString(value.toString()))
                            if not self.isTemporary(children.item(x)):
                                self.markAsDirty()
            else:
                #print "New text node to be added"
                # We need to add a text node since it was blank
                if value.toString() != QString(""):
                    newText = self.domDocument.createTextNode(QString(value.toString()))
                    domNode.appendChild(newText)
                    if not self.isTemporary(newText):
                        self.markAsDirty()
        return True

    def makeEditable(self,node):
        # Strip the inherited attribute down the tree
        self.stripAttributeDown('inherited',node)
        # if we are not a temporary node then we need to also strip up
        # the tree... temp nodes can be made editable without affecting parents
        if not self.isTemporary(node):
            # Now up the tree, only hitting parent nodes and not sibblings
            self.stripAttributeUp('inherited',node)

    def insertRow(self,row,parent,node,editable=True):
        returnval = QAbstractItemModel.insertRow(self,row,parent)
        self.beginInsertRows(parent,row,row)
        # Add the element
        if parent == QModelIndex():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        if parentItem.numChildren() == 0:
            parentItem.domNode.appendChild(node)
        elif row >= parentItem.numChildren():
            parentItem.domNode.insertAfter(node, parentItem.lastChild().domNode)
        else:
            parentItem.domNode.insertBefore(node, parentItem.child(row).domNode)

        nodeElement = node.toElement()
        if not nodeElement.isNull():
            # Check if it is hidden... and if so we skip it in the visible tree
            if not nodeElement.hasAttribute(QString("flags")) or \
                   nodeElement.attribute(QString("flags")) != QString("hidden"):
                item = SettingsDataItem(self.domDocument,node,row,parentItem)
                item.initAsRootItem()
                #print "len=%d row=%d" % (len(parentItem.childItems),row)
                parentItem.childItems.insert(row,item)
        self.endInsertRows()
        if editable:
            self.makeEditable(node)
        if not self.isTemporary(node):
            self.markAsDirty()
        return returnval

    def removeRow(self,row,parent,checkInherited=True):
        returnval = QAbstractItemModel.removeRow(self,row,parent)
        self.beginRemoveRows(parent,row,row)
        # Remove the element
        if parent == QModelIndex():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        nodeToRemove = parentItem.child(row).domNode
        domNodePath = self.domNodePath(nodeToRemove)
        parentItem.domNode.removeChild(nodeToRemove)
        parentItem.childItems.pop(row)
        if not self.isTemporary(nodeToRemove):
            self.markAsDirty()
            # Now check if it was inherited and the original should
            # be added back in
            #if checkInherited:
                #self.checkIfInheritedAndAddBackToTree(domNodePath, parent)
        self.endRemoveRows()
        return returnval

    def moveUp(self,item,howmany=1):
        if item.isValid():
            currentRow = item.row()
            if currentRow > 0:
                if howmany > currentRow:
                    howmany = currentRow
                clone = item.internalPointer().domNode.cloneNode()
                currentParent = item.parent()
                self.removeRow(currentRow,currentParent,False)
                self.insertRow(currentRow-howmany,currentParent,clone)
                self.markAsDirty()

    def moveDown(self,item,howmany=1):
        if item.isValid():
            currentRow = item.row()
            if item.parent() == QModelIndex():
                parentItem = self._rootItem
            else:
                parentItem = item.parent().internalPointer()
            if currentRow < parentItem.numChildren()-1:
                if howmany > (parentItem.numChildren()-1) - currentRow:
                    howmany = (parentItem.numChildren()-1) - currentRow
                clone = item.internalPointer().domNode.cloneNode()
                currentParent = item.parent()
                self.removeRow(currentRow,currentParent,False)
                self.insertRow(currentRow+howmany,currentParent,clone)
                if not self.isTemporary(item.internalPointer().domNode):
                    self.markAsDirty()

    def findElementIndexByName(self,name,parent,multiple=False):
        finds = []
        rows = self.rowCount(parent)
        for x in xrange(0,rows,1):
            child = self.index(x,0,parent)
            childElement = child.internalPointer().domNode.toElement()
            if not childElement.isNull():
                # Check if this is the one we want...
                if childElement.nodeName() == QString(name):
                    finds.append(child)
                    if multiple == False:
                        return finds
                # If this child has other children then we recurse
                if self.rowCount(child)>0:
                    childSearch = self.findElementIndexByName(name,child,multiple)
                    if multiple == False:
                        #Check to make sure there is only one in the list returned
                        if len(childSearch) != 1:
                            print "Error in search... multiple returns when single expected"
                        if childSearch[0] != QModelIndex():
                            return childSearch
                    else:
                        finds.extend(childSearch)
        if len(finds) == 0:
            finds.append(QModelIndex())
        return finds

    def findElementIndexByType(self,name,parent,multiple=False):
        finds = []
        rows = self.rowCount(parent)
        for x in xrange(0,rows,1):
            child = self.index(x,0,parent)
            childElement = child.internalPointer().domNode.toElement()
            if not childElement.isNull():
                # Check if this is the one we want...
                if childElement.hasAttribute(QString("type")) and \
                       childElement.attribute(QString("type")) == QString(name):
                    finds.append(child)
                    if multiple == False:
                        return finds
                # If this child has other children then we recurse
                if self.rowCount(child)>0:
                    childSearch = self.findElementIndexByType(name,child,multiple)
                    if multiple == False:
                        #Check to make sure there is only one in the list returned
                        if len(childSearch) != 1:
                            print "Error in search... multiple returns when single expected"
                        if childSearch[0] != QModelIndex():
                            return childSearch
                    else:
                        finds.extend(childSearch)
        if len(finds) == 0:
            finds.append(QModelIndex())
        return finds

    # This function needs to be tested... but is here for the future
    #def stripAttribute(self,attribute,parent,recursive=True):
    #    rows = self.rowCount(parent)
    #    for x in xrange(0,rows,1):
    #        child = self.index(x,0,parent)
    #        childElement = child.internalPointer().domNode.toElement()
    #        if not childElement.isNull():
    #            # Check if this is the one we want...
    #            if childElement.hasAttribute(QString(attribute)):
    #                # remove the attribute
    #                childElement.removeAttribute(QString(attribute))
    #                if recursive == False:
    #                    return
    #            # If this child has other children then we recurse
    #            if self.rowCount(child)>0:
    #                self.stripAttribute(attribute,child,recursive)

    def create_node(self, document, name, type, value = "", choices = None, temporary = False, flags = None):
        newNode = document.createElement(QString(name))
        newNode.setAttribute(QString("type"),QString(type))
        
        if value != "":
            if type == 'list':
                newText = document.createTextNode(QString(str(value)))
            else:
                newText = document.createTextNode(QString(value))
            newNode.appendChild(newText)        
        if choices is not None:
            newNode.setAttribute(QString('choices'), QString(choices))
        if temporary is True:
            newNode.setAttribute(QString("temporary"),QString("True"))
        if flags is not None:
            newNode.setAttribute(QString('flags'), QString(flags))
        return newNode

    def stripAttributeDown(self,attribute,parent):
        parentElement = parent.toElement()
        if not parentElement.isNull():
            if parentElement.hasAttribute(QString(attribute)):
                # remove the attribute
                parentElement.removeAttribute(QString(attribute))
                if not self.isTemporary(parentElement):
                    self.markAsDirty()
            rows = parent.childNodes().count()
            for x in xrange(0,rows,1):
                child = parent.childNodes().item(x)
                childElement = child.toElement()
                if not childElement.isNull():
                    # Check if this is the one we want...
                    if childElement.hasAttribute(QString(attribute)):
                        # remove the attribute
                        childElement.removeAttribute(QString(attribute))
                        if not self.isTemporary(childElement):
                            self.markAsDirty()
                    # If this child has other children then we recurse
                    childRows = child.childNodes().count()
                    if childRows>0:
                        self.stripAttributeDown(attribute,child)
        return parent

    def stripAttributeUp(self,attribute,parent):
        parentElement = parent.toElement()
        if not parentElement.isNull():
            if parentElement.hasAttribute(QString(attribute)):
                # remove the attribute
                parentElement.removeAttribute(QString(attribute))
                if not self.isTemporary(parentElement):
                    self.markAsDirty()
            grandParent = parent.parentNode()
            if not grandParent.isNull():
                self.stripAttributeUp(attribute,grandParent)
        return parent
    
    
class SettingsDataItem:
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
                childItem = SettingsDataItem(self.domDocument,childNode, i , self)
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
                childItem = SettingsDataItem(self.domDocument,childNode, i , self)
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
