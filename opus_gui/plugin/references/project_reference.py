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

from enthought.traits.api import HasTraits, Any

from enthought.envisage import get_application
from enthought.envisage.single_project.api import IPROJECT_MODEL
import logging
logger = logging.getLogger(__name__)

from envisage_demo.model.person import Person

class ProjectReference(HasTraits):    
    type = Any
    obj = Any
    
    def create_resource(self):
        return
#        try:
#            # hack
#            project_model = get_application().get_service(IPROJECT_MODEL)
#            
#            current_project = project_model.project
#            
#    #        if self.type is Person:
#            for person in current_project.persons:
#                if person.name == self.obj.name:
#                    return person
#            
#            return Person(name='Something wrong', age=999)
#        
#        except Exception, e:
#            print e
#            return Person(name='Something wrong', age=999)