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

from enthought.pyface.action.api import Action

from opus_gui.model.person import Person

class NewPersonAction(Action):
    def perform(self, event):
        subcontext = event.node.obj
        
        name = subcontext.get_unique_name('New Person')
        
        person = Person(name=name, age=0)
        subcontext.project.persons.append(person)