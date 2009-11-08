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
A monitor for Persons nodes.

"""

# Standard library imports
import logging

# Enthought library imports
from enthought.naming.api import Binding
from enthought.pyface.tree.api import NodeMonitor


# Setup a logger for this module
logger = logging.getLogger(__name__)


class PersonsSubcontextMonitor(NodeMonitor):
    """
    A monitor for PersonsSubcontext nodes.

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
        Add or remove trait change handlers to/from a Persons.

        """
#
#        logger.debug('%s trait listeners for Persons [%s] '
#            'in GeoContextNodeMonitor [%s]',
#            (remove and 'Removing' or 'Adding'), project, self)

        # Update the node if the list of persons changes.
        subcontext.project.on_trait_change(self._on_persons_changed, 'persons',
            remove=remove)
        subcontext.project.on_trait_change(self._on_persons_items_changed, 'persons_items',
            remove=remove)

        return

    #### Trait change handlers ###############################################
#
#    def _on_name_changed(self, obj, name, old, new):
#        """
#        Handle the Persons' name changing.
#
#        """
#
#        logger.debug('Name changed in PersonsSubcontextMonitor [%s]', self)
#
#        self.node.name = new
#        self.fire_nodes_changed()
#
#        return


    def _on_persons_changed(self, old, new):
        """
        Handle the 's list of persons changing.

        """

#        logger.debug('Persons changed in PersonsSubcontextMonitor [%s]', self)

        # Update the model for the changes
        old_bindings = [Binding(name=o.name, obj=o) for o in old]
        new_bindings = [Binding(name=o.name, obj=o, context=self.node.obj) for o in new]
        self.fire_nodes_replaced(old_bindings, new_bindings)

        return

    def _on_persons_items_changed(self, event):
        """
        Handle additions and removals to the 's list of persons.

        """

#        logger.debug('Persons items changed in PersonsSubcontextMonitor [%s]',
#            self)

        # Create a context to represent the monitored Persons.
        ctx = self.node.obj

        # Remove the nodes representing the removed persons.
        old_bindings = [Binding(name=o.name, obj=o) for o in event.removed]
        self.fire_nodes_removed(old_bindings)

        # Insert nodes to represent the new persons.  Each person should
        # be inserted into the same position it would be in if the context for
        # the project was regenerated.
        for o in event.added:
            binding = Binding(name=o.name, obj=o, context=ctx)
            index = ctx.get_node_index(o)
            self.fire_nodes_inserted([binding], index=index)

        return


#### EOF #####################################################################

