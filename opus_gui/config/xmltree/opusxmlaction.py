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
from PyQt4.QtCore import QObject, SIGNAL

from opus_gui.general_manager.controllers.xml_action_general import xmlActionController_General
from opus_gui.results_manager.controllers.xml_action_results import xmlActionController_Results
from opus_gui.models_manager.controllers.xml_action_models import xmlActionController_Models
from opus_gui.scenarios_manager.controllers.xml_action_scenarios import xmlActionController_Scenarios
from opus_gui.data_manager.controllers.xml_action_data import xmlActionController_Data
#from opus_gui.data_manager.opusxmlaction_datadb import OpusXMLAction_DataDB

class OpusXMLAction(object):
    def __init__(self, xmlTreeObject):
        self.xmlTreeObject = xmlTreeObject
        self.mainwindow = xmlTreeObject.mainwindow

        self.actionObject = self.getXMLActionObjectByType(self.xmlTreeObject.xmlType)
        if self.actionObject:
            QObject.connect(self.xmlTreeObject.view,
                            SIGNAL("customContextMenuRequested(const QPoint &)"),
                            self.actionObject.processCustomMenu)

    def getXMLActionObjectByType(self,xmlType):
        if xmlType == "results_manager":
            return xmlActionController_Results(self)
        elif xmlType == "model_manager":
            return xmlActionController_Models(self)
        elif xmlType == "scenario_manager":
            return xmlActionController_Scenarios(self)
        elif xmlType == "data_manager":
            return xmlActionController_Data(self)
#        elif xmlType == "data_manager_dbstree":
#            return OpusXMLAction_DataDB(self)
        elif xmlType == "general":
            return xmlActionController_General(self)
        else:
            #error out
            return None
