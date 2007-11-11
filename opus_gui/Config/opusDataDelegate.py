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
from opusDataModel import OpusDataModel
from opusDataItem import OpusDataItem

class OpusDataDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        if index.column() == 2:
            #model = index.model()
            #btobject = model.getItemAt(index.row())
            editor = QComboBox(parent)
            print "here1"
            return editor
        else:
            print "here2"
            return QItemDelegate.createEditor(self, parent, option, index)
    
    def setEditorData(self,editor,index):
        #print "here3"
        pass
    
    def setModelData(self,editor,model,index):
        pass
    
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
