#
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

from enthought.traits.api import Instance
from enthought.envisage.workbench.api import TraitsUIEditor

from opus_gui.model.model_specification_list import ModelSpecificationList

class ModelSpecificationListEditor(TraitsUIEditor):
    resource = Instance(ModelSpecificationList)
    
    def _resource_changed(self):
        self.name = self.resource.name
        
    def _name_changed_for_resource(self, old, new):
        self.name = self.resource.name