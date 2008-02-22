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

class OpusDataDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        self.parent = parent
        self.signalMapper = QSignalMapper(self)
        
    def createEditor(self, parent, option, index):
        if not index.isValid():
            return QItemDelegate.createEditor(self, parent, option, index)
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        if domNode.isNull():
            return QItemDelegate.createEditor(self, parent, option, index)
        # Handle ElementNodes
        if domNode.isElement():
            domElement = domNode.toElement()
            if domElement.isNull():
                return QItemDelegate.createEditor(self, parent, option, index)
            # So we have a valid element and our column is 2 we need to make a editor
            if index.column() == 2:
                if domElement.hasAttribute(QString("choices")):
                    editor = QComboBox(parent)
                    choices = domElement.attribute(QString("choices"))
                    currentIndex = 0
                    for i,choice in enumerate(choices.split("|")):
                        editor.addItem(choice)
                        if index.model().data(index,Qt.DisplayRole).toString() == choice:
                            currentIndex = i
                    editor.setCurrentIndex(currentIndex)
                    QObject.connect(editor, SIGNAL("activated(int)"), self.comboBoxFinished)
                    return editor
                elif domElement.attribute(QString("type")) == QString("db_connection_hook"):
                    editor = QComboBox(parent)
                    # Now find the options from the database section of the XML
                    dbxml = self.parent.parent.toolboxStuff.dataManagerDBSTree.model.index(0,0,QModelIndex()).parent()
                    dbindexlist = self.parent.parent.toolboxStuff.dataManagerDBSTree.model.findElementIndexByType("db_connection",dbxml,True)
                    choices = []
                    for dbindex in dbindexlist:
                        if dbindex.isValid():
                            indexElement = dbindex.internalPointer()
                            choices.append(indexElement.domNode.toElement().tagName())
                    currentIndex = 0
                    for i,choice in enumerate(choices):
                        editor.addItem(choice)
                        if index.model().data(index,Qt.DisplayRole).toString() == choice:
                            currentIndex = i
                    editor.setCurrentIndex(currentIndex)
                    QObject.connect(editor, SIGNAL("activated(int)"), self.comboBoxFinished)
                    return editor                    
                else:
                    editor = QItemDelegate.createEditor(self, parent, option, index)
                    if type(editor) == QLineEdit:
                        editor.setText(index.model().data(index,Qt.DisplayRole).toString())
                    return editor
            elif index.column() == 0:
                editor = QItemDelegate.createEditor(self, parent, option, index)
                if type(editor) == QLineEdit:
                    editor.setText(index.model().data(index,Qt.DisplayRole).toString())
                return editor
            else:
                return QItemDelegate.createEditor(self, parent, option, index)
    
    def setEditorData(self,editor,index):
        pass
        
    
    def setModelData(self,editor,model,index):
        #print "setModelData"
        if type(editor) == QComboBox:
            model.setData(index,QVariant(editor.currentText()),Qt.EditRole)
        else:
            QItemDelegate.setModelData(self,editor,model,index)
        
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def comboBoxFinished(self,x):
        #print "comboBoxFinished ", self.sender()
        self.emit(SIGNAL("commitData(QWidget*)"),self.sender())
