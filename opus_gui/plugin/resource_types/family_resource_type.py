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

from opus_gui.plugin.node_types.family_node_type import FamilyNodeType
from opus_gui.plugin.editors.family_editor import FamilyEditor
from opus_gui.plugin.references.project_reference import ProjectReference

from opus_gui.model.family import Family


class FamilyResourceType(ResourceType):
    """
    The resource type for our project resources.

    """

    ##########################################################################
    # Traits
    ##########################################################################

    #### public 'ResourceType' interface #####################################

    # A trait that describes the kind of domain object that the type
    # represents.
    type = Instance(Family)

    editor = FamilyEditor

    ##########################################################################
    # 'ResourceType' interface.
    ##########################################################################

    #### Initializers ########################################################

    def _node_type_default(self):
        """
        Initializes the node type.

        """
        return FamilyNodeType(resource_type=self)

    def get_reference(self, obj):
        return ProjectReference(type=Family, obj=obj)
        
#### EOF #####################################################################