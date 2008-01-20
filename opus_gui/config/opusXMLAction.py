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

from config.resultsmanager.opusXMLAction_Results import OpusXMLAction_Results
from config.modelmanager.opusXMLAction_Model import OpusXMLAction_Model
from config.scenariomanager.opusXMLAction_Scenario import OpusXMLAction_Scenario
from config.datamanager.opusXMLAction_Data import OpusXMLAction_Data

class OpusXMLAction(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlTreeObject = parent
        
        self.actionObject = self.getXMLActionObjectByType(self.xmlTreeObject.xmlType)
        QObject.connect(self.xmlTreeObject.view, SIGNAL("customContextMenuRequested(const QPoint &)"),
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
        else:
            #error out
            pass
