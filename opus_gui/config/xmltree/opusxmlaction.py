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
from PyQt4.QtCore import *

from opus_gui.config.generalmanager.opusxmlaction_general import OpusXMLAction_General
from opus_gui.config.resultsmanager.opusxmlaction_results import OpusXMLAction_Results
from opus_gui.config.modelmanager.opusxmlaction_model import OpusXMLAction_Model
from opus_gui.config.scenariomanager.opusxmlaction_scenario import OpusXMLAction_Scenario
from opus_gui.config.datamanager.opusxmlaction_data import OpusXMLAction_Data
#from opus_gui.config.datamanager.opusxmlaction_datadb import OpusXMLAction_DataDB

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
            return OpusXMLAction_Results(self)
        elif xmlType == "model_manager":
            return OpusXMLAction_Model(self)
        elif xmlType == "scenario_manager":
            return OpusXMLAction_Scenario(self)
        elif xmlType == "data_manager":
            return OpusXMLAction_Data(self)
#        elif xmlType == "data_manager_dbstree":
#            return OpusXMLAction_DataDB(self)
        elif xmlType == "general":
            return OpusXMLAction_General(self)
        else:
            #error out
            return None
