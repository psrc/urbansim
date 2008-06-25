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

class OpusAllVariablesDelegate(QItemDelegate):
    def __init__(self, parentView):
        QItemDelegate.__init__(self, parentView)
        self.parentView = parentView
        self.signalMapper = QSignalMapper(self)
        
    def createEditor(self, parentView, option, index):
        if not index.isValid():
            return QItemDelegate.createEditor(self, parentView, option, index)
        editor = QItemDelegate.createEditor(self, parentView, option, index)
        if type(editor) == QLineEdit:
            editor.setText(index.model().data(index,Qt.DisplayRole).toString())
            return editor
        else:
            return QItemDelegate.createEditor(self, parentView, option, index)

    def setEditorData(self,editor,index):
        pass

    def setModelData(self,editor,model,index):
        QItemDelegate.setModelData(self,editor,model,index)

    def updateEditorGeometry(self, editor, option, index):
        QItemDelegate.updateEditorGeometry(self,editor,option,index)
        
