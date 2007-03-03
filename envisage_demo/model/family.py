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

from enthought.traits.api import HasTraits, List, Str, Instance, Property, \
    View, Item, Group, EnumEditor

from envisage_demo.model.person import Person

class Family(HasTraits):
    name = Str
    husband = Instance(Person)
    wife = Instance(Person)
    children = List
    context = Instance('envisage_demo.model.project.Project')
    
    persons = Property
    
    def _get_persons(self):
        return dict([
            (person, person.name)
            for person in self.context.persons
            ])
    
    def __init__(self, *args, **kwargs):
        HasTraits.__init__(self, *args, **kwargs)
        
        if self.context is None:
            raise NameError('The context parameter must be defined.')
    
    def _persons_changed_for_context(self):
        self.trait_property_changed('persons', [], self.persons)
        
        # def _prersons_changed_for_context(self, old, new):
        #   <do the above>
        #
        # Add listeners on each person's name
        # self._update_listeners_on_person(new, remove=False)
        # Remove old listeners on persons no longer in the list
        # self._update_listeners_on_person(old, remove=True)
    
    def _persons_items_changed_for_context(self):
        self.trait_property_changed('persons', [], self.persons)
        
        # def _persons_items_changed_for_context(self, event):
        # <do the above>
        # self._update_listeners_on_persons(event.added, remove=False)
        # Add listeners on each person's name
        # Remove old listeners on persons no longer in the list
        # self._update_listeners_on_persons(event.removed, remove=True)
    
    
    # def _update_listeners_on_persons(self, list, remove):
    #     for o in list:
    #        o.on_trait_change(self._on_person_name_changed, 'name', remove=remove)
    
    # def _on_person_name_changed(self):
    #    self.trait_property_changed('persons', [], self.persons)
    
    
    my_view = View(
        Item('name', width=300),
        Item('husband', editor=EnumEditor(name='persons')),
        Item('wife', editor=EnumEditor(name='persons')),
        Item('children'),
        )