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
#from PyQt4.QtCore import Qt
from opus_gui.abstract_manager.controllers.xml.opus_xml_controller import OpusXMLController
#from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
#from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
#from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate

class DatabaseConfigXMLController(OpusXMLController):
    def __init__(self, toolboxbase, xmlType, parentWidget, addTree=True):
        OpusXMLController.__init__(self, toolboxbase = toolboxbase, xml_type = xmlType, parentWidget = parentWidget, addTree = addTree, listen_to_menu = False)
        
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