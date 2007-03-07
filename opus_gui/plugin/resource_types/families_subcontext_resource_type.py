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

# Local imports.
from opus_gui.plugin.node_types.families_subcontext_node_type import FamiliesSubcontextNodeType

from opus_gui.plugin.project_context_adapter import FamiliesSubcontext

class FamiliesSubcontextResourceType(ResourceType):
    """
    The resource type for our project resources.

    """

    ##########################################################################
    # Traits
    ##########################################################################

    #### public 'ResourceType' interface #####################################

    # A trait that describes the kind of domain object that the type
    # represents.
    type = Instance(FamiliesSubcontext)


    ##########################################################################
    # 'ResourceType' interface.
    ##########################################################################

    #### Initializers ########################################################

    def _node_type_default(self):
        """
        Initializes the node type.

        """
        return FamiliesSubcontextNodeType(resource_type=self)


#### EOF #####################################################################