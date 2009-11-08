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

from envisage_demo.plugin.node_types.person_node_type import PersonNodeType
from envisage_demo.plugin.editors.person_editor import PersonEditor
from envisage_demo.plugin.references.project_reference import ProjectReference

from envisage_demo.model.person import Person


class PersonResourceType(ResourceType):
    """
    The resource type for our project resources.

    """

    ##########################################################################
    # Traits
    ##########################################################################

    #### public 'ResourceType' interface #####################################

    # A trait that describes the kind of domain object that the type
    # represents.
    type = Instance(Person)

    editor = PersonEditor

    ##########################################################################
    # 'ResourceType' interface.
    ##########################################################################

    #### Initializers ########################################################

    def _node_type_default(self):
        """
        Initializes the node type.

        """
        return PersonNodeType(resource_type=self)

    def get_reference(self, obj):
        return ProjectReference(type=Person, obj=obj)
        
#### EOF #####################################################################