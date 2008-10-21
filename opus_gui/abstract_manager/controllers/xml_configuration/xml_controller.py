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
from PyQt4.QtCore import QObject, SIGNAL, Qt, QString
from PyQt4.QtGui import QAction

from opus_gui.abstract_manager.views.xml_view import XmlView
from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.abstract_manager.models.xml_item_delegate import XmlItemDelegate


class XmlController(object):
    def __init__(self, toolboxbase, xml_type, parentWidget):
        
        self.toolboxbase = toolboxbase
        self.mainwindow = toolboxbase.mainwindow
        self.xmlType = xml_type
        self.parentWidget = parentWidget
        
        self.model = None
        self.view = None
        self.delegate = None
        
        # default model, view and delegate
        self.setupModelViewDelegate()
        self.setupWidget()


    def setupModelViewDelegate(self):
        '''bind the model, view and delegate to this controller. 
        Override for inheriting classes that want to use different 
        controller items.'''
        self.model = XmlModel(self, self.toolboxbase.doc, self.mainwindow,
                      self.toolboxbase.configFile, self.xmlType, True)
        self.view = XmlView(self.mainwindow)
        self.delegate = XmlItemDelegate(self.view)

        
    def setupWidget(self):
        '''setup the view and add it to the parent widget'''
        self.view.setItemDelegate(self.delegate)
        self.view.setModel(self.model)
        
        # Need to traverse the whole tree and expand the nodes if they default to open
        self.view.openDefaultItems()


        self.parentWidget.addWidget(self.view)

        # Hook up to the mousePressEvent and pressed
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self.view,
                        SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.processCustomMenu)
        
    def createAction(self, icon, text, callback):
        '''convenience method to create actions''' 
        action = QAction(icon, text, self.mainwindow)
        QObject.connect(action, SIGNAL('triggered()'), callback)
        return action
        
    def removeTree(self):
        if not self.model.isDirty():
            self.view.hide()
            self.parentWidget.removeWidget(self.view)
            return True
        else:
            return False

    def processCustomMenu(self, position):
        raise Exception('Method processCustomMenu is not implemented')

