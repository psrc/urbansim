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


"""
The resource type for our project resources.

"""

# Enthought library imports
from enthought.envisage.resource import ResourceType
from enthought.traits.api import Instance

from opus_gui.model.model_specification_list import ModelSpecificationList

from opus_gui.plugin.references.project_reference import ProjectReference
from opus_gui.plugin.editors.model_specification_list_editor import ModelSpecificationListEditor
from opus_gui.plugin.node_types.model_specification_list_node_type import ModelSpecificationListNodeType


class ModelSpecificationListResourceType(ResourceType):
    """
    The resource type for our project resources.
    """

    type = Instance(ModelSpecificationList)
    editor = ModelSpecificationListEditor

    def _node_type_default(self):
        """
        Initializes the node type.
        """
        return ModelSpecificationListNodeType(resource_type=self)

    def get_reference(self, obj):
        return ProjectReference(type=ModelSpecificationList, obj=obj)