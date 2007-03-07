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

""" The entry point for an Envisage application. """


# Standard library imports.
import sys

# Enthought library imports.
from enthought.envisage.workbench.api import WorkbenchApplication

# Local imports.
from envisage_demo.plugins_to_use import INCLUDE, PLUGIN_DEFINITIONS


# fixme: We need to put this inside a function 'cos there is some wierdness by
# which 'gui' becomes a module after calling 'application.start'! It is to do
# with how we load plugin definitions (by calling 'execfile'). It seems that it
# effects the global namespace. This needs looking into! Most applications
# don't notice this 'cos they set 'requires_gui' to be True and let Envisage
# create the 'GUI' instance, but this is an experiment into how it really
# should be!
def run(argv):
    """ Runs the application. """

    # Create the application.
    application = WorkbenchApplication(
        argv = argv,
        id = 'envisage_demo',
        include = INCLUDE,
        plugin_definitions = PLUGIN_DEFINITIONS
    )

    # Run the application (this starts the application, starts the GUI event
    # loop, and when that terminates, stops the application).
    application.run()

    return


# Application entry point.
if __name__ == '__main__':
    run(sys.argv)


#### EOF ######################################################################
