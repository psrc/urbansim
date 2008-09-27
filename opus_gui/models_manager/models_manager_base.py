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

from opus_gui.models_manager.controllers.tabs.estimation_gui_element import EstimationGuiElement
from opus_gui.abstract_manager.abstract_manager_base import AbstractManagerBase

class ModelsManagerBase(AbstractManagerBase):
    def __init__(self, mainwindow):
        AbstractManagerBase.__init__(self, mainwindow = mainwindow)

    def addEstimationElement(self,model):
        self.addNewGuiElement(EstimationGuiElement(self.mainwindow,self,model))
