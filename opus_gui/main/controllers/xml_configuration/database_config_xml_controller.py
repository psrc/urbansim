# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController

class DatabaseConfigXMLController(XmlController):
    def __init__(self, manager):
        XmlController.__init__(manager)

    def process_custom_menu(self, position):
        pass

# TODO: Adding / removing databases ?

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