#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class size_category(Variable):
    """Create categories accoring to the sizes of projects"""
    
    def dependencies(self):
        return [my_attribute_label("project_id")]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.categorize(attribute_name=ds.attribute_name, bins=ds.categories)+1
