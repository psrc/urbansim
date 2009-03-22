# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

# PyQt4 includes for python bindings to QT
#from PyQt4.QtCore import Qt
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
#from opus_gui.abstract_manager.views.xml_view import XmlView
#from opus_gui.abstract_manager.models.xml_model import OpusDataModel
#from opus_gui.abstract_manager.models.xml_item_delegate

class DatabaseConfigXMLController(XmlController):
    def __init__(self, manager):
        XmlController.__init__(manager)

    def processCustomMenu(self, position):
        pass # to avoid raising not implemented error

#    def addTree(self):
#        self.model = DatabaseConfigXMLModel(self, self.toolboxbase.doc, self.mainwindow,
#                                   self.toolboxbase.configFile, self.xmlType, True)


#class DatabaseConfigXMLModel(OpusDataModel):
#    def __init__(self, parentTree, document, mainwindow, configFile, xmlType, editable, addIcons=True):
#        OpusDataModel.__init__(self, parentTree, document, mainwindow, configFile, xmlType, editable, addIcons)
#
#    def flags(self, index):
#        default_flags = super(DatabaseConfigXMLModel, self).flags(index)
#        if index.isValid() and self.editable and index.column()==0:
#            return default_flags & ~Qt.ItemIsEditable
#        else: return default_flags