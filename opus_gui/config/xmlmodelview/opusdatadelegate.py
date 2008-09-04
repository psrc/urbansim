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
from PyQt4.QtGui import *
from PyQt4.QtXml import *

class OpusDataDelegate(QItemDelegate):
    def __init__(self, parentView):
        QItemDelegate.__init__(self, parentView)
        self.parentView = parentView
        self.signalMapper = QSignalMapper(self)
        
    def createEditor(self, parentView, option, index):
        if not index.isValid():
            return QItemDelegate.createEditor(self, parentView, option, index)
        # Get the item associated with the index
        item = index.internalPointer()
        domNode = item.node()
        if domNode.isNull():
            return QItemDelegate.createEditor(self, parentView, option, index)
        # Handle ElementNodes
        if domNode.isElement():
            domElement = domNode.toElement()
            if domElement.isNull():
                return QItemDelegate.createEditor(self, parentView, option, index)
            # So we have a valid element and our column is 1 we need to make a editor
            if index.column() == 1:
                if domElement.hasAttribute(QString("choices")):
                    editor = QComboBox(parentView)
                    choices = domElement.attribute(QString("choices"))
                    currentIndex = 0
                    for i,choice in enumerate(choices.split("|")):
                        editor.addItem(choice)
                        if index.model().data(index,Qt.DisplayRole).toString() == choice:
                            currentIndex = i
                    editor.setCurrentIndex(currentIndex)
                    #QObject.connect(editor, SIGNAL("activated(int)"), self.comboBoxFinished)
                    return editor
                elif domElement.attribute(QString("type")) == QString("db_connection_hook"):
                    editor = QComboBox(parentView)
                    # Now find the options from the database section of the XML
                    dbxml = self.parentView.mainwindow.toolboxStuff.dataManagerDBSTree.model.index(0,0,QModelIndex()).parent()
                    dbindexlist = self.parentView.mainwindow.toolboxStuff.dataManagerDBSTree.model.findElementIndexByType("db_connection",dbxml,True)
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
                    return editor                    
                elif domElement.attribute(QString("type")) == QString("file_path") or \
                         domElement.attribute(QString("type")) == QString("dir_path"):
                    # We have a file path we need to fill in...
                    editor_file = QFileDialog()
                    filter_str = QString("*.*")
                    editor_file.setFilter(filter_str)
                    editor_file.setAcceptMode(QFileDialog.AcceptOpen)
                    if domElement.attribute(QString("type")) == QString("file_path"):
                        fd = editor_file.getOpenFileName(self.parentView.mainwindow,QString("Please select a file..."),
                                                         index.model().data(index,Qt.DisplayRole).toString())
                    elif domElement.attribute(QString("type")) == QString("dir_path"):
                        fd = editor_file.getExistingDirectory(self.parentView.mainwindow,QString("Please select a directory..."),
                                                              index.model().data(index,Qt.DisplayRole).toString())                        
                    # Check for cancel
                    if len(fd) == 0:
                        fileName = index.model().data(index,Qt.DisplayRole).toString()
                    else:
                        fileName = QString(fd)
                    editor = QItemDelegate.createEditor(self, parentView, option, index)
                    if type(editor) == QLineEdit:
                        editor.setText(fileName)
                    return editor
                elif domElement.attribute(QString("type")) == QString("password"):
                    editor = QLineEdit(parentView)
                    editor.setEchoMode(QLineEdit.PasswordEchoOnEdit)
                    valueToDisplay = QString("")
                    if domElement.hasChildNodes():
                        children = domElement.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                valueToDisplay = children.item(x).nodeValue()
                                break
                    editor.setText(valueToDisplay)
                    return editor
                else:
                    editor = QItemDelegate.createEditor(self, parentView, option, index)
                    if type(editor) == QLineEdit:
                        editor.setText(index.model().data(index,Qt.DisplayRole).toString())
                    return editor
            elif index.column() == 0:
                editor = QItemDelegate.createEditor(self, parentView, option, index)
                if type(editor) == QLineEdit:
                    editor.setText(index.model().data(index,Qt.DisplayRole).toString())
                return editor
            else:
                return QItemDelegate.createEditor(self, parentView, option, index)

    def setEditorData(self,editor,index):
        pass

    def setModelData(self,editor,model,index):
        #print "setModelData"
        if type(editor) == QComboBox:
            model.setData(index,QVariant(editor.currentText()),Qt.EditRole)
        else:
            QItemDelegate.setModelData(self,editor,model,index)

    def updateEditorGeometry(self, editor, option, index):
        if type(editor) == QComboBox:
            editor.setGeometry(option.rect)
        else:
            QItemDelegate.updateEditorGeometry(self,editor,option,index)
        
