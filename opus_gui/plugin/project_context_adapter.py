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

from enthought.naming.api import Context
from enthought.envisage.resource import ResourceContextAdapter
from enthought.traits.api import Instance, View

from opus_gui.model.project import Project
from opus_gui.model.family import Family
from opus_gui.model.person import Person

class ProjectContextAdapter(ResourceContextAdapter):
    ###########################################################################
    # Protected 'Context' interface.
    ###########################################################################
    def _lookup(self, name):
        """ Looks up a name in this context. """
        
            
        return None
    
    def _is_bound(self, name):
        return name in self._list_names()
    
    def _bind(self, name, obj):
        """ Binds a name to an object in this context. """
        # Used for drag & drop, etc.
        

    def _unbind(self, name):
        """ Unbinds a name from this context. """

        

    def _rename(self, old_name, new_name):
        """ Renames an object in this context. """


    def _create_subcontext(self, name):
        """ Creates a sub-context of this context. """
        return

    def _destroy_subcontext(self, name):
        """ Destroys a sub-context of this context. """
        return

    def _list_names(self):
        """ Lists the names bound in this context. """

        return [
            ]

    def _is_context(self, name):
        """ Returns True if a name is bound to a context. """
        return True