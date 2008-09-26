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

from opus_gui.scenarios_manager.controllers.simulation_gui_element import SimulationGuiElement
from opus_gui.abstract_manager.abstract_manager_base import AbstractManagerBase

class ScenariosManagerBase(AbstractManagerBase):
    def __init__(self, mainwindow):
        AbstractManagerBase.__init__(self, mainwindow = mainwindow)

    def addNewSimulationElement(self,model):
        self.addNewGuiElement(SimulationGuiElement(self.mainwindow,self,model))