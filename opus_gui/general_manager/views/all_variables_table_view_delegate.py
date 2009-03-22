# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 


# PyQt4 includes for python bindings to QT

from PyQt4.QtCore import QSignalMapper, Qt, QVariant
from PyQt4.QtGui import QItemDelegate, QCheckBox, QComboBox, QTextOption, QTextEdit

class AllVariablesTableViewDelegate(QItemDelegate):
    def __init__(self, parentView):
        QItemDelegate.__init__(self, parentView)
        self.parentView = parentView
        self.signalMapper = QSignalMapper(self)
        
    def createEditor(self, parentView, option, index):
        if not index.isValid():
            return QItemDelegate.createEditor(self, parentView, option, index)
        if index.column() == 100:
            print "Trying to create QCheckbox"
            editor = QCheckBox(parentView)
            checkBool = index.model().data(index,Qt.DisplayRole).toBool()
            if checkBool:
                editor.setCheckState(Qt.Checked)
            else:
                editor.setCheckState(Qt.Unchecked)
        elif index.column() == 3:
            # Column 3 is "Use" with options "model variable", "indicator", or "both"
            editor = QComboBox(parentView)
            choices = ["both", "model variable", "indicator"]
            currentIndex = 0
            for i,choice in enumerate(choices):
                editor.addItem(choice)
                if index.model().data(index,Qt.DisplayRole).toString() == choice:
                    currentIndex = i
            editor.setCurrentIndex(currentIndex)
            #editor.setMinimumContentsLength(20)
            #editor.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            return editor
        elif index.column() == 4:
            # Column 4 is "Source" with options "primary attribute", "expression", "Python class"
            editor = QComboBox(parentView)
            choices = ["primary attribute","expression","Python class"]
            currentIndex = 0
            for i,choice in enumerate(choices):
                editor.addItem(choice)
                if index.model().data(index,Qt.DisplayRole).toString() == choice:
                    currentIndex = i
            editor.setCurrentIndex(currentIndex)
            #editor.setMinimumContentsLength(20)
            #editor.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            return editor
        else:
            #editor = QItemDelegate.createEditor(self, parentView, option, index)
            #if type(editor) == QLineEdit:
            #    editor.setText(index.model().data(index,Qt.DisplayRole).toString())
            editor = QTextEdit(parentView)
            editor.setAcceptRichText(False)
            editor.setWordWrapMode(QTextOption.WrapAnywhere)
            editor.setText(index.model().data(index,Qt.DisplayRole).toString())
        return editor

    def setEditorData(self,editor,index):
        pass

    def setModelData(self,editor,model,index):
        if type(editor) == QComboBox:
            model.setData(index,QVariant(editor.currentText()),Qt.EditRole)
        elif type(editor) == QTextEdit:
            model.setData(index,QVariant(editor.toPlainText()),Qt.EditRole)
        else:
            QItemDelegate.setModelData(self,editor,model,index)

    def updateEditorGeometry(self, editor, option, index):
        if type(editor) == QComboBox:
            newRect = option.rect
            newRect.adjust(-30,0,30,0)
            editor.setGeometry(newRect)
        elif type(editor) == QTextEdit:
            newRect = option.rect
            newRect.adjust(-5,-7,-5,7)
            editor.setGeometry(newRect)
        else:
            QItemDelegate.updateEditorGeometry(self,editor,option,index)
        
