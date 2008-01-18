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
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from opusDataItem import OpusDataItem

class OpusDataBaseModel(object):
    def __init__(self, parent, document, configFile):
        self.parent = parent
        self.document = document
        self.configFile = configFile

        self._rootItem = OpusDataItem(document, 0, self)
        self._rootItem.initAsRootItem()

        # Dirty flag for keeping track of edits...
        self.dirty = False

    def findRootElement(self,tag):
        pass
        


class OpusDataModel(QAbstractItemModel):
    def __init__(self, parentTree, document, parent, configFile, xmlType, editable):
        QAbstractItemModel.__init__(self, parent)
        self.parentTree = parentTree
        self.editable = editable
        self.configFile = configFile
        self.parentObj = parent
        self.domDocument = document
        self.xmlType = xmlType
        # Dirty flag for keeping track of edits...
        self.dirty = False
        
        # Root data for use in column headers
        self.rootData = []
        self.rootData.append(QVariant("Name"))
        self.rootData.append(QVariant("Type"))
        self.rootData.append(QVariant("Value"))

        # Get the XML config data
        self.xmlRoot = document.elementsByTagName(QString(self.xmlType)).item(0)
        print "Searching for ", self.xmlType
        if self.xmlRoot == None:
            print "No XML elements in the root with type ", self.xmlType
            return
        print "Found ", self.xmlRoot.nodeName()
        #self._rootItem = OpusDataItem(document,document.documentElement(), 0, self)
        self._rootItem = OpusDataItem(document,self.xmlRoot, 0, self)
        # Loop through the first level children and inti them as a root item
        # and append to the tree...
        for x in xrange(0,self.xmlRoot.childNodes().count(),1):
            current = self.xmlRoot.childNodes().item(x)
            self._rootItemSub = OpusDataItem(document,current, x, self._rootItem)
            self._rootItemSub.initAsRootItem()
            self._rootItem.childItems.append(self._rootItemSub)
        
        #Add some icons
        self.folderIcon = QIcon()
        self.bookmarkIcon = QIcon()
        
        self.app = qApp

        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.bulletIcon = QIcon(":/Images/Images/bullet_black.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.carIcon = QIcon(":/Images/Images/car.png")
        self.chartBarIcon = QIcon(":/Images/Images/chart_bar.png")
        self.chartLineIcon = QIcon(":/Images/Images/chart_line.png")
        self.chartOrgIcon = QIcon(":/Images/Images/chart_organisation.png")
        self.cogIcon = QIcon(":/Images/Images/cog.png")
        self.databaseLinkIcon = QIcon(":/Images/Images/database_link.png")
        self.databaseIcon = QIcon(":/Images/Images/database.png")
        self.databaseTableIcon = QIcon(":/Images/Images/database_table.png")
        self.errorIcon = QIcon(":/Images/Images/error.png")
        self.exclamationIcon = QIcon(":/Images/Images/exclamation.png")
        self.fieldIcon = QIcon(":/Images/Images/field.png")
        self.folderDatabaseIcon = QIcon(":/Images/Images/folder_database.png")
        self.folderIcon = QIcon(":/Images/Images/folder.png")
        self.layersIcon = QIcon(":/Images/Images/layers.png")
        self.lockIcon = QIcon(":/Images/Images/lock.png")
        self.mapGoIcon = QIcon(":/Images/Images/map_go.png")
        self.mapIcon = QIcon(":/Images/Images/map.png")
        self.pageWhiteIcon = QIcon(":/Images/Images/page_white.png")
        self.pythonScriptIcon = QIcon(":/Images/Images/python_script.png")
        self.pythonTypeIcon = QIcon(":/Images/Images/python_type.png")
        self.tableGoIcon = QIcon(":/Images/Images/table_go.png")
        self.tableLightningIcon = QIcon(":/Images/Images/table_lightning.png")
        self.tableMultipleIcon = QIcon(":/Images/Images/table_multiple.png")
        self.tableIcon = QIcon(":/Images/Images/table.png")
        
        self.bookmarkIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_FileIcon))        
        self.folderIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_DirClosedIcon),
                                  QIcon.Normal, QIcon.Off)
        self.folderIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_DirOpenIcon),
                                  QIcon.Normal, QIcon.On)
        self.bookmarkIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_FileIcon))

    def findXMLRoot(self,doc,tp):
        i = 0
        childNode = None
        for x in xrange(0,doc.childNodes().count(),1):
            current = doc.childNodes().item(x)
            print "FOO",current.attributes().namedItem(QString("type")).nodeValue()
            if (current.attributes().namedItem(QString("type")).nodeValue() == QString(tp)) and (current.nodeType() == QDomNode.ElementNode):
                childNode = current
        return childNode
    
    def iconFromType(self, attType):
        typeMap = {"string":self.fieldIcon,
                   "path":self.folderDatabaseIcon,
                   "directory":self.pythonTypeIcon,
                   "file":self.pageWhiteIcon,
                   "class":self.pythonTypeIcon,
                   "dictionary":self.pythonScriptIcon,
                   "list":self.pythonTypeIcon,
                   "tuple":self.pythonTypeIcon,
                   "unicode":self.fieldIcon,
                   "integer":self.fieldIcon,
                   "float":self.fieldIcon,
                   "model":self.cogIcon,
                   "dataset":self.folderDatabaseIcon,
                   "table":self.tableIcon,
                   "password":self.lockIcon,
                   "checkbox":self.bulletIcon,
                   "cacheConfig":self.databaseLinkIcon,
                   "boolean":self.pythonTypeIcon,
                   "":self.bulletIcon}
        if attType != QString("defValue") and typeMap.has_key(str(attType)):
            return typeMap[str(attType)]
        else:
            return QVariant()
    
    # We only allow for one child colum per branch in the tree
    def columnCount(self, parent):
        #return 1
        return 3

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
                    return QVariant(self.iconFromType(domElement.attribute(QString("type"))))
                elif role == Qt.DisplayRole:
                    return QVariant(domElement.tagName())
                else:
                    return QVariant()
            elif index.column() == 1:
                if role == Qt.DecorationRole:
                    return QVariant()
                elif role == Qt.DisplayRole:
                    return QVariant(domElement.attribute(QString("type")))
                else:
                    return QVariant()
            elif index.column() == 2:
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
        else:
            print "Node is not handled yet in the OpusDataModel - ", str(domNode.nodeType())
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if self.editable == True:
            if index.column() == 2:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled
        
    
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

    def setData(self,index,value,role):
        
        if not index.isValid():
            return False
        if role != Qt.EditRole:
            return False
        print "ModelView setData %s" % (value.toString())
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        if domNode.hasChildNodes():
            children = domNode.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    children.item(x).setNodeValue(QString(value.toString()))
                    if self.dirty == False:
                        self.parentTree.groupBox.setTitle(self.parentTree.groupBox.title().prepend(QString("*")))
                    self.dirty = True
        return True

    def insertRow(self,row,parent,node):
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
        item = OpusDataItem(self.domDocument,node,row,parentItem)
        item.initAsRootItem()
        #print "len=%d row=%d" % (len(parentItem.childItems),row)
        parentItem.childItems.insert(row,item)
        self.endInsertRows()
        #print "debug"
        return returnval

    def removeRow(self,row,parent):
        returnval = QAbstractItemModel.removeRow(self,row,parent)
        self.beginRemoveRows(parent,row,row)
        # Remove the element
        if parent == QModelIndex():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        parentItem.domNode.removeChild(parentItem.child(row).domNode)
        parentItem.childItems.pop(row)
        self.endRemoveRows()
        return returnval

    def moveUp(self,item):
        if item.isValid():
            currentRow = item.row()
            if currentRow > 0:
                clone = item.internalPointer().domNode.cloneNode()
                currentParent = item.parent()
                self.removeRow(currentRow,currentParent)
                self.insertRow(currentRow-1,currentParent,clone)
    
    def moveDown(self,item):
        if item.isValid():
            currentRow = item.row()
            if item.parent() == QModelIndex():
                parentItem = self._rootItem
            else:
                parentItem = item.parent().internalPointer()
            if currentRow < parentItem.numChildren()-1:
                clone = item.internalPointer().domNode.cloneNode()
                currentParent = item.parent()
                self.removeRow(currentRow,currentParent)
                self.insertRow(currentRow+1,currentParent,clone)
