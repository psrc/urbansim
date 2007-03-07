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

class PersonsSubcontext(Context):
    project = Instance(Project)
    
    def _list_names(self):
        """ Lists the names bound in this context. """

        return [
            person.name 
            for person in self.project.persons
            ]
            
    def _lookup(self, name):
        for person in self.project.persons:
            if person.name == name:
                return person
            
        return None
        
    def get_node_index(self, obj):
        for index in range(len(self.project.persons)):
            if self.project.persons[index] is obj:
                return index
            
    my_view = View() # hack


class FamiliesSubcontext(Context):
    project = Instance(Project)
    
    def _list_names(self):
        """ Lists the names bound in this context. """

        return [
            family.name 
            for family in self.project.families
            ]
            
    def _lookup(self, name):
        for family in self.project.families:
            if family.name == name:
                return family
            
        return None
        
    def get_node_index(self, obj):
        for index in range(len(self.project.families)):
            if self.project.families[index] is obj:
                return index
            
    my_view = View()

class ProjectContextAdapter(ResourceContextAdapter):
    ###########################################################################
    # Protected 'Context' interface.
    ###########################################################################
    def _lookup(self, name):
        """ Looks up a name in this context. """
        
        if name == 'Persons':
            return PersonsSubcontext(project=self.adaptee)
        elif name == 'Families':
            return FamiliesSubcontext(project=self.adaptee)
        
        # Check persons
        for person in self.adaptee.persons:
            if person.name == name:
                return person
        
        # Check families
        for family in self.adaptee.families:
            if family.name == name:
                return family
            
        return None
    
    def _is_bound(self, name):
        return name in self._list_names()
    
    def _bind(self, name, obj):
        """ Binds a name to an object in this context. """
        # Used for drag & drop, etc.
        
        # Is a family?
        if isinstance(obj, Family):
            # Check for duplicates
            #    get unique name...
            self.adaptee.families.append(obj)
            
        # Is a person?
        if isinstance(obj, Person):
            # Check for duplicates
            #    get unique name...
            self.adaptee.persons.append(obj)

    def _unbind(self, name):
        """ Unbinds a name from this context. """

        for person in self.adaptee.persons:
            if person.name == name:
                self.adaptee.persons.remove(person)

        for family in self.adaptee.families:
            if family.name == name:
                self.adaptee.families.remove(family)

    def _rename(self, old_name, new_name):
        """ Renames an object in this context. """

        for person in self.adaptee.persons:
            if person.name == old_name:
                person.name = new_name
                
        for family in self.adaptee.families:
            if family.name == old_name:
                family.name = new_name

    def _create_subcontext(self, name):
        """ Creates a sub-context of this context. """
        return

    def _destroy_subcontext(self, name):
        """ Destroys a sub-context of this context. """
        return

    def _list_names(self):
        """ Lists the names bound in this context. """

        return [
            'Persons',
            'Families',
            ]

    def _is_context(self, name):
        """ Returns True if a name is bound to a context. """
        return True