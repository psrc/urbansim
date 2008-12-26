#
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

from PyQt4.QtCore import QVariant, QString, Qt, QModelIndex, SIGNAL
from PyQt4.QtGui import QColor

from opus_gui.abstract_manager.models.xml_model import XmlModel

class XmlModel_Models(XmlModel):
    
    def __init__(self, parentTree, document, mainwindow, configFile, xmlType, 
                 editable, addIcons=True):
        XmlModel.__init__(self, parentTree, document, mainwindow, configFile, 
                          xmlType, editable, addIcons)

    def data(self, index, role):
        #override visual representation of some data types
        element = index.internalPointer().node().toElement()
        element_type = element.attribute('type')
        
        # only override displaying of left column
        if index.column() != 0:
            return QVariant()
        
        if role == Qt.DisplayRole:
            if element_type == 'model_system':
                return QVariant(QString('Models'))
            elif element_type == 'model':
                return QVariant(element.tagName())
                # maybe return a nicer name?
            elif element_type == 'configuration':
                return QVariant(QString('Estimation Configuration'))
        elif role == Qt.ForegroundRole:
            if element_type == 'configuration':
                return QVariant(QColor(Qt.darkMagenta))
        # fall back on default
        return XmlModel.data(self, index, role)

    def insert_model(self, model_element):
        '''inserts a dom element under model_system'''
        # find the model_system node
        model_system_index = None
        for row in xrange(0, self.rowCount(None)):
            index = self.index(row, 0, QModelIndex())
            element = index.internalPointer().node().toElement()  
            if element.tagName() == 'model_system':
                model_system_index = index
                break
        if not model_system_index:
            print "Warning! Could not find model_system in tree. " \
                  "Unable to insert model."
            return
        
        self.insertRow(self.rowCount(model_system_index), 
                       model_system_index, 
                       model_element)
        self.emit(SIGNAL('layoutChanged()'))
