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

from enthought.envisage import PluginDefinition

#from opus_gui.plugin.actions.default_action import DefaultAction

from enthought.envisage.action.action_plugin_definition import Menu
from enthought.envisage.action.action_plugin_definition import Group
from enthought.envisage.action.action_plugin_definition import Action
from enthought.envisage.action.action_plugin_definition import Location
from enthought.envisage.action.action_plugin_definition import ActionSet

from enthought.envisage.workbench.workbench_plugin_definition import View
from enthought.envisage.workbench.workbench_plugin_definition import Workbench
from enthought.envisage.workbench.workbench_plugin_definition import Perspective

from enthought.envisage.resource.resource_plugin_definition import ResourceType
from enthought.envisage.resource.resource_plugin_definition import ResourceManager

from enthought.envisage.single_project.plugin_definition import FactoryDefinition
from enthought.envisage.single_project.plugin_definition import SyncProjectSelection

from enthought.envisage.repository.repository_extensions import ExportableObject
from enthought.envisage.repository.repository_extensions import RepositoryRootFactory

##############################################################################
# Constants
##############################################################################

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = 'opus_gui.plugin'

##############################################################################
# Extension points.
##############################################################################

class EnvisageDemoActionSet(ActionSet):
    """
    Action and menu definitions for the project view.
    """

    # A mapping from human-readable root names to globally unique Ids.
    aliases = {
#        'FamilyMenu' : ID + '.family_menu',
        }
    
#class EditFamilyAction(DefaultAction):
#    name = 'Edit family...'    
#    tooltip = 'Edit this family.'
#    description = 'Edit this family.'

opus_gui_action_set = EnvisageDemoActionSet(
    id = ID + '.opus_gui_action_set',
    name = 'EnvisageDemoActionSet',

    groups = [
#        Group(
#            id = 'PersonsMenuGroup',
#            location = Location(path='PersonsMenu')
#            ),
        ],

    actions = [
#        NewPersonAction(
#            locations = [
#                Location(path='PersonsMenu/PersonsMenuGroup'),
#                ],
#            ),
        ],
    )

#### Workbench Perspectives and Views ########################################

workbench = Workbench(
    perspectives = [
        ],

    views = [
#        View(
#            uol = 'import://opus_gui.plugin.views.selected_traits_view.selected_traits_view',
#            id = ID + '.selected_traits_view',
#            name = 'Selected Traits View',
#            ),
        ],
    )

#### Factory Definitions #####################################################

factory_definition = FactoryDefinition(
    class_name = ID + '.project_factory.ProjectFactory',
    priority = 10,
    )


#### Resources ###############################################################

resource_manager = ResourceManager(
    resource_types = [
        ResourceType(
            class_name = ID + '.resource_types.project_resource_type.ProjectResourceType',
            precedes   = [
                'enthought.envisage.single_project.project_resource_type.ProjectResourceType',
                ]
            ),
        ResourceType(
            class_name = ID + '.resource_types.model_specification_list_resource_type.ModelSpecificationListResourceType',
            precedes   = [
                'enthought.envisage.resource.instance_resource_type.InstanceResourceType',
                'enthought.envisage.resource.folder_resource_type.FolderResourceType',
                ]
            ),
        ],
    )

##############################################################################
# The plugin definition.
##############################################################################

class ProjectPluginDefinition(PluginDefinition):
    # The plugin's globally unique identifier.
    id = ID

    # The name of the class that implements the plugin.

    # General information about the plugin.
    name = 'Opus Gui Project Plugin'
    version = '0.0.1'
    provider_name = 'CUSPA'
    provider_url = 'www.urbansim.org'
    autostart = True

    # The Id's of the plugins that this plugin requires.
    requires = [
        ]

    # The extension points offered by this plugin.
    extension_points = [
        EnvisageDemoActionSet,
        ]

    # The contributions that this plugin makes to extension points offered by
    # either itself or other plugins.
    extensions = [
        resource_manager,
        factory_definition,
        opus_gui_action_set,
        workbench,
#        SyncProjectSelection(name='selection', uol='import://opus_gui.plugin.views.selected_traits_view.selected_traits_view'),
        ]


#### EOF #######################################################################