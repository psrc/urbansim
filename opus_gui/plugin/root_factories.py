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

from enthought.envisage.repository.template_repository_root_factory import TemplateRepositoryRootFactory

class BuiltInRootFactory(TemplateRepositoryRootFactory):
    name = 'EnvisageDemoBuiltInRootFactory'
    
    path = './data'
    
    class_name = 'opus_gui.plugin.root_factories.BuiltInRootFactory'
    
    def roots(self):        
        ret = super(BuiltInRootFactory, self).roots()
        
        return ret