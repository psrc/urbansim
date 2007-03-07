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
from enthought.envisage.repository.api import IREPOSITORY

from opus_gui.model.person import Person


class ImportPersonAction(Action):
    def perform(self, event):
        service = get_application().get_service(IREPOSITORY)
        
        person = service.import_object('opus_gui.plugin.resource_types.person_resource_type.PersonResourceType')
        
        subcontext = event.node.obj
        
        subcontext.project.persons.append(person)