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
A monitor for envisage_demo nodes.

"""

# Standard library imports
import logging

# Enthought library imports
from enthought.naming.api import Binding
from enthought.pyface.tree.api import NodeMonitor


# Setup a logger for this module
logger = logging.getLogger(__name__)


class FamiliesSubcontextMonitor(NodeMonitor):
    """
    A monitor for FamiliesSubcontext nodes.

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

    def _setup_trait_change_handlers(self, subcontext, remove=False):
        """
        Add or remove trait change handlers to/from a project.

        """

        # Update the node if the list of families changes.
        subcontext.project.on_trait_change(self._on_families_changed, 'families',
            remove=remove)
        subcontext.project.on_trait_change(self._on_families_items_changed, 'families_items',
            remove=remove)

        return

    #### Trait change handlers ###############################################
#
#    def _on_name_changed(self, obj, name, old, new):
#        """
#        Handle the family's name changing.
#
#        """
#
#        logger.debug('Name changed in Families list [%s]', self)
#
#        self.node.name = new
#        self.fire_nodes_changed()
#
#        return


    def _on_families_changed(self, old, new):
        """
        Handle the project's list of families changing.

        """

#        logger.debug('Families changed in Families list [%s]', self)

        # Update the model for the changes
        old_bindings = [Binding(name=o.name, obj=o) for o in old]
        new_bindings = [Binding(name=o.name, obj=o, context=self.node.obj) for o in new]
        self.fire_nodes_replaced(old_bindings, new_bindings)

        return

    def _on_families_items_changed(self, event):
        """
        Handle additions and removals to the project's list of families.

        """

#        logger.debug('Families items changed in Families list [%s]',
#            self)

        # Create a context to represent the monitored Families.
        ctx = self.node.obj

        # Remove the nodes representing the removed families.
        old_bindings = [Binding(name=o.name, obj=o) for o in event.removed]
        self.fire_nodes_removed(old_bindings)

        # Insert nodes to represent the new families.  Each family should
        # be inserted into the same position it would be in if the context for
        # the project was regenerated.
        for o in event.added:
            binding = Binding(name=o.name, obj=o, context=ctx)
            index = ctx.get_node_index(o)
            self.fire_nodes_inserted([binding], index=index)

        return


#### EOF #####################################################################

