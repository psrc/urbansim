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

""" The list of plugin definitions that make up the application.

All this module does is create a list of absolute filenames! The ONLY reason we
keep it separate from 'run.py' is that it tends to contain a fair bit of path
manipulation shenanigans that make 'run.py' a bit hard to read.

"""

# Enthought library imports.
from enthought.envisage import join

# We use the enthought package to find the absolute location of other
# packages.
import enthought

# Application imports
import envisage_demo.plugin


# The plugin definitions that make up the application.
PLUGIN_DEFINITIONS = [
    # Core plugins.
    join(enthought, 'envisage/core/core_plugin_definition.py'),
    join(enthought, 'envisage/resource/resource_plugin_definition.py'),
    join(enthought, 'envisage/action/action_plugin_definition.py'),
    join(enthought, 'envisage/workbench/workbench_plugin_definition.py'),
    join(enthought, 'envisage/workbench/action/action_plugin_definition.py'),

    # Our chosen project framework's plugins
    join(enthought, 'envisage/single_project/plugin_definition.py'),

    # Enthought plugins.
    join(enthought, 'plugins/python_shell/python_shell_plugin_definition.py'),
    join(enthought, 'plugins/text_editor/text_editor_plugin_definition.py'),
    # repository plugin
    join(enthought, 'envisage/repository/repository_plugin_definition.py'),
    # logger plugin
    join(enthought, 'logger/plugin/logger_plugin_definition.py'),
          
    # Debugging.
    #join(enthought, 'developer/fbi_plugin_definition.py'),
    #join(enthought, 'developer/plugin_definition.py'),
    #join(enthought, 'envisage/internal/internal_plugin_definition.py'),

    # Opus Application Plugins
    #join(XXX,'YYYY/plugin_definition.py'),
    join(envisage_demo.plugin, 'plugin_definition.py'),
    ]


# The plugin definitions that we want to import from but don't want as part of
# the application.
INCLUDE = []


#### EOF ######################################################################
