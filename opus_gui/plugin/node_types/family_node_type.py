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
The node type associated with our project resources.

"""

# Standard library imports.
import logging

# Enthought library imports
from enthought.envisage import get_application
from enthought.envisage.resource import ResourceNodeType
from enthought.pyface.api import ImageResource

# Setup a logger for this module.
logger = logging.getLogger(__name__)


from envisage_demo.plugin.monitors.family_monitor import FamilyMonitor


class FamilyNodeType(ResourceNodeType):
    """
    The node type associated with our project resources.

    """
    
    def get_monitor(self, node):
        return FamilyMonitor(node=node)
    
    ##########################################################################
    # Traits
    ##########################################################################

    #### public 'ResourceNodeType' interface #################################

    # If set, then we build our context menu by querying for actions, groups,
    # and menus, within ActionSets, which are configured for locations starting
    # with this path.
    action_location_root = 'envisage_demo.plugin.family_menu'


    #### public 'NodeType' interface #########################################

    # The image used to represent nodes of this type that are NOT expanded.
#    closed_image = ImageResource('close_project')

    # The image used to represent nodes of this type that ARE expanded.
#    open_image = ImageResource('open_project')


    ##########################################################################
    # 'NodeType' interface
    ##########################################################################

    ##########################################################################
    # 'ResourceNodeType' interface
    ##########################################################################

    #### protected interface #################################################

    def _get_action_sets(self):
        """
        Returns all action set contributions.

        """

        from envisage_demo.plugin.plugin_definition import EnvisageDemoActionSet
        
        action_sets = get_application().load_extensions(EnvisageDemoActionSet)
        logger.debug('Found contribution action sets:')
        for set in action_sets:
            logger.debug('  Name: [%s]', set.name)

        return action_sets

    def _default_action_default(self):
        from envisage_demo.plugin.actions.edit_family_action import EditFamilyAction
        return EditFamilyAction()

    def allows_children(self, node):
        return False

#### EOF #####################################################################
