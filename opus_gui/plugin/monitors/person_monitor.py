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
A monitor for Person nodes.

"""

# Standard library imports
import logging

# Enthought library imports
from enthought.naming.api import Binding
from enthought.pyface.tree.api import NodeMonitor


# Setup a logger for this module
logger = logging.getLogger(__name__)


class PersonMonitor(NodeMonitor):
    """
    A monitor for Person nodes.

    """

    ##########################################################################
    # 'NodeMonitor' interface.
    ##########################################################################

    def start(self):
        """
        Start listening to changes to the node.

        """
        if self.node.obj is not None:
            self._setup_trait_change_handlers(self.node.obj)

        return

    def stop(self):
        """
        Stop listening to changes to the node.

        """

        if self.node.obj is not None:
            self._setup_trait_change_handlers(self.node.obj, remove=True)

        return

    ##########################################################################
    # Private interface
    ##########################################################################

    def _setup_trait_change_handlers(self, person, remove=False):
        """
        Add or remove trait change handlers to/from a Person.

        """

        # Update the node if the name of the person changes.
        person.on_trait_change(self._on_name_changed, 'name', remove=remove)

        return

    #### Trait change handlers ###############################################
#
    def _on_name_changed(self, obj, name, old, new):
        """
        Handle the person's name changing.

        """
        
        self.node.name = new
        self.fire_nodes_changed()

        return

#### EOF #####################################################################

