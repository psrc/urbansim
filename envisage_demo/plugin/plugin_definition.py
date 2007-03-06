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
from enthought.envisage.single_project.plugin_definition import FactoryDefinition, SyncProjectSelection
from enthought.envisage.resource.resource_plugin_definition import \
    ResourceManager, ResourceType
from enthought.envisage.action.action_plugin_definition import \
    Action, ActionSet, Group, Location, Menu
from envisage_demo.plugin.actions.default_action import DefaultAction
from enthought.envisage.workbench.workbench_plugin_definition import \
    Perspective, View, Workbench
from enthought.envisage.repository.repository_extensions import RepositoryRootFactory, ExportableObject
##############################################################################
# Constants
##############################################################################

# The plugin's globally unique identifier (also used as the prefix for all
# identifiers defined in this module).
ID = 'envisage_demo.plugin'

##############################################################################
# Extension points.
##############################################################################

class EnvisageDemoActionSet(ActionSet):
    """
    Action and menu definitions for the project view.

    """

    # A mapping from human-readable root names to globally unique Ids.
    aliases = {
        'PersonsMenu' : ID + '.persons_menu',
        'PersonMenu' : ID + '.person_menu',
        'FamiliesMenu' : ID + '.families_menu',
        }

class NewPersonAction(DefaultAction):
    name = 'New person...'    
    tooltip = 'Create a new person.'
    description = 'Create a new person.'
    
class ImportPersonAction(DefaultAction):
    name = 'Import person...'    
    tooltip = 'Import a person.'
    description = 'Import a person.'
    
class ExportPersonAction(DefaultAction):
    name = 'Export person...'    
    tooltip = 'Export a person.'
    description = 'Export a person.'
    
class EditPersonAction(DefaultAction):
    name = 'Edit person...'    
    tooltip = 'Edit this person.'
    description = 'Edit this person.'
    
class NewFamilyAction(DefaultAction):
    name = 'New family...'    
    tooltip = 'Create a new family.'
    description = 'Create a new family.'

envisage_demo_action_set = EnvisageDemoActionSet(
    id = ID + '.envisage_demo_action_set',
    name = 'EnvisageDemoActionSet',

    groups = [
        Group(
            id = 'PersonsMenuGroup',
            location = Location(path='PersonsMenu')
            ),
        Group(
            id = 'PersonMenuGroup',
            location = Location(path='PersonMenu')
            ),
        Group(
            id = 'FamiliesMenuGroup',
            location = Location(path='FamiliesMenu')
            ),
        ],

    actions = [
        NewPersonAction(
            locations = [
                Location(path='PersonsMenu/PersonsMenuGroup'),
                ],
            ),
        EditPersonAction(
            locations = [
                Location(path='PersonMenu/PersonMenuGroup'),
                ],
            ),
        Action( # Export person
            class_name="enthought.envisage.repository.action.export_selection.ExportSelection",
            description='Export person...',
            name = 'Export Person',
            id = 'ExportPerson',
            locations = [
                Location(path='PersonMenu/PersonMenuGroup', after='EditPerson'),
                ],
            ),
        ImportPersonAction(
            locations = [
                Location(path='PersonsMenu/PersonsMenuGroup', after='NewPerson'),
                ],
            ),
        NewFamilyAction(
            locations = [
                Location(path='FamiliesMenu/FamiliesMenuGroup'),
                ],
            ),
        ],
    )

exportable_person = ExportableObject(
    class_name = 'envisage_demo.model.person.Person',
    id = 'envisage_demo.model.person.Person',
    label = 'Person Template',
    )

#### Workbench Perspectives and Views ########################################

workbench = Workbench(
    perspectives = [
#        Perspective(
#            id = ID + '.perspective.project',
#            name = 'Project',
#            contents = [
#                Perspective.Item(
#                    id = ID + '.view.project_view.ProjectView',
#                    position = 'left',
#                    width = 0.25,
#                    ),
#                Perspective.Item(
#                    id = 'enthought.plugins.python_shell.view.PythonShellView',
#                    position = 'bottom',
#                    width = 0.75,
#                    ),
#                ]
#            ),
        ],

    views = [
#        View(
#            id         = ID + '.views.selected_traits_view.SelectedTraitsView',
#            class_name = ID + '.views.selected_traits_view.SelectedTraitsView',
##            image      = 'images/view.png',
#            name       = 'Selected Traits View',
#            position   = 'right',
#            ),
        View(
            uol = 'import://envisage_demo.plugin.views.selected_traits_view.selected_traits_view',
            id = ID + '.selected_traits_view',
            name = 'Selected Traits View',
            ),
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
            class_name = ID + '.project_resource_type.ProjectResourceType',
            precedes   = [
                'enthought.envisage.single_project.project_resource_type.ProjectResourceType',
                ]
            ),
        ResourceType(
            class_name = ID + '.resource_types.persons_subcontext_resource_type.PersonsSubcontextResourceType',
            precedes   = [
                'enthought.envisage.resource.instance_resource_type.InstanceResourceType',
                'enthought.envisage.resource.folder_resource_type.FolderResourceType',
                ]
            ),
        ResourceType(
            class_name = ID + '.resource_types.person_resource_type.PersonResourceType',
            precedes   = [
                'enthought.envisage.resource.instance_resource_type.InstanceResourceType',
                'enthought.envisage.resource.folder_resource_type.FolderResourceType',
                ]
            ),
        ResourceType(
            class_name = ID + '.resource_types.families_subcontext_resource_type.FamiliesSubcontextResourceType',
            precedes   = [
                'enthought.envisage.resource.instance_resource_type.InstanceResourceType',
                'enthought.envisage.resource.folder_resource_type.FolderResourceType',
                ]
            ),
        ResourceType(
            class_name = ID + '.resource_types.family_resource_type.FamilyResourceType',
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
    version = '1.0.0'
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
        envisage_demo_action_set,
        workbench,
        SyncProjectSelection(name='selection', uol='import://envisage_demo.plugin.views.selected_traits_view.selected_traits_view'),
        RepositoryRootFactory(class_name='envisage_demo.plugin.root_factories.BuiltInRootFactory'),
        exportable_person,
        ]


#### EOF #####################################################################
