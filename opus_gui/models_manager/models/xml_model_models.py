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
from opus_gui.abstract_manager.models.xml_item import XmlItem


class XmlModel_Models(XmlModel):
    
    # tag name for estimation configuration
    estimation_config_tag_name = 'estimation_config'
    
    #TODO: icons for Models / Estimations
    def __init__(self, parentTree, document, mainwindow, configFile, xmlType, 
                 editable, addIcons=True):
        XmlModel.__init__(self, parentTree, document, mainwindow, configFile, 
                          xmlType, editable, addIcons)

    def data_handler(self, index, role):
        '''override the displaying of xml nodes'''
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
        return QVariant()

    def build_item_tree_from_root(self):
        '''override the default tree building to make sure estimate_config 
        is in top'''
        child_nodes = [e for e in self.child_elements(self.xmlRoot)]
        # move estimation_config to first slot
        if QString('estimation_config') in child_nodes:
            idx = child_nodes.index(self.estimation_config_tag_name)
            child_nodes.insert(0, child_nodes.pop(child_nodes.index(idx)))

        for e in child_nodes:
            if not e.isNull():
                item = XmlItem(self.domDocument, e, self._rootItem)
                item.initAsRootItem()
                self._rootItem.childItems.append(item)

    def insert_model(self, model_element):
        '''inserts a dom element under model_system'''
        # insert last under the first node
        model_system_index = self.index(0, 0, QModelIndex())
        self.insertRow(self.rowCount(model_system_index), 
                       model_system_index, 
                       model_element)
        self.emit(SIGNAL('layoutChanged()'))
