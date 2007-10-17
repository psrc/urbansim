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

class OpusDataModel(QAbstractItemModel):
    def __init__(self, document, parent):
        QAbstractItemModel.__init__(self, parent)

        self.parentObj = parent
        self.domDocument = document
        
        # Root data for use in column headers
        self.rootData = []
        self.rootData.append(QVariant("Storage"))
        self.rootData.append(QVariant("Type"))

        # Get the XML config data
        self._rootItem = OpusDataItem(document,0,self)
        
        #Add some icons
        self.folderIcon = QIcon()
        self.bookmarkIcon = QIcon()
        
        self.app = qApp

        self.database = QIcon(":/Images/Images/database.png")
        self.database_link = QIcon(":/Images/Images/database_link.png")
        self.database_table = QIcon(":/Images/Images/database_table.png")
        self.folder = QIcon(":/Images/Images/folder.png")
        self.python_script = QIcon(":/Images/Images/python_script.png")

        self.bookmarkIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_FileIcon))
        
        self.folderIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_DirClosedIcon),
                                  QIcon.Normal, QIcon.Off)
        self.folderIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_DirOpenIcon),
                                  QIcon.Normal, QIcon.On)
        self.bookmarkIcon.addPixmap(self.app.style().standardPixmap(QStyle.SP_FileIcon))

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
        #if domNode.isElement() and domNode.nodeType() == QDomNode.ElementNode:
        # Handle ElementNodes
        if domNode.isElement():
            domElement = domNode.toElement()
            if domElement.isNull():
                return QVariant()
            if index.column() == 0:
                if role == Qt.DecorationRole:
                    return QVariant(self.folderIcon)
                elif role == Qt.DisplayRole:
                    if domElement.parentNode().nodeName() == "str":
                        #Do something with strings
                        return (domElement.text())
                    elif domElement.parentNode().nodeName() == "int":
                        #Do something with numbers
                        return (domElement.text())
                    elif domElement.tagName() != "":
                        return QVariant(domElement.tagName())
                    else:
                        return QVariant()
                else:
                    return QVariant()
            elif index.column() == 1:
                return QVariant()
            else:
                #We have a problem... should only be 2 columns
                print "Wrong number of columns"
                return QVariant()
        # Handle TextNodes
        elif domNode.nodeType() == QDomNode.TextNode:
            if role == Qt.DecorationRole:
                if index.column() == 0:
                    return QVariant(self.bookmarkIcon)
                else:
                    return QVariant()
            elif role == Qt.DisplayRole:
                if index.column() == 1:
                    if domNode.parentNode().nodeName() == "str":
                        #Do something with strings
                        return QVariant(domNode.parentNode().nodeName())
                    elif domNode.parentNode().nodeName() == "int":
                        #Do something with numbers
                        return QVariant(domNode.parentNode().nodeName())
                    else:
                        return QVariant(QString("str"))
                else:
                    return QVariant(domNode.nodeValue())
            else:
                return QVariant()
        # Handle CommentNode
        elif domNode.nodeType() == QDomNode.CommentNode:
            if role == Qt.DecorationRole:
                if index.column() == 0:
                    return QVariant(self.bookmarkIcon)
                else:
                    return QVariant()
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return QVariant(domNode.nodeValue())
                else:
                    return QVariant()
            else:
                return QVariant()
        # Handle ProcessingInstructionNodes
        elif domNode.nodeType() == QDomNode.ProcessingInstructionNode:
            if role == Qt.DecorationRole:
                if index.column() == 0:
                    return QVariant(self.folderIcon)
                else:
                    return QVariant()
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return QVariant(domNode.nodeValue())
                else:
                    return QVariant()
            else:
                return QVariant()
        else:
            print "Node is not handled yet in the OpusDataModel - ", str(domNode.nodeType())
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return 0
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        #return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
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
        return self.createIndex(parentItem.row(),0,parentItem)
    
    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        parentItem = None
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.node().childNodes().count()

    def setData(self,index,value,role):
        print "setData %s" % (value.toString())
        
        if not index.isValid():
            return False
        if role != Qt.EditRole:
            return False
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        domNode.setNodeValue(QString(value.toString()))
        indentSize = 2
        self.parentObj.configFile.close()
        self.parentObj.configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
        out = QTextStream(self.parentObj.configFile)
        self.domDocument.save(out, indentSize)
        return True
