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

import sys

from enthought.envisage.workbench.api import WorkbenchApplication

from opus_gui.plugins_to_use import INCLUDE, PLUGIN_DEFINITIONS


def run(argv):
    """ Runs the application. """

    application = WorkbenchApplication(
        argv = argv,
        id = 'opus_gui',
        include = INCLUDE,
        plugin_definitions = PLUGIN_DEFINITIONS,
        )

    application.run()


if __name__ == '__main__':
    run(sys.argv)