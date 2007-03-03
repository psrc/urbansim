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
from enthought.envisage.workbench.api import IWORKBENCH

from envisage_demo.model.person import Person


class EditPersonAction(Action):
    def perform(self, event):
        person = event.node.obj
        
        workbench = event.application.get_service(IWORKBENCH)
        
        workbench.edit(person)