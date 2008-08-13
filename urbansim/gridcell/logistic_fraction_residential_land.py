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

from opus_core.variables.variable import Variable, ln_bounded
from variable_functions import my_attribute_label

class logistic_fraction_residential_land(Variable):
    """Natural log of the total_value for this gridcell"""
    
    _return_type="float32"  
    
    def dependencies(self):
        return [my_attribute_label('fraction_residential_land')]
        
    def compute(self, dataset_pool):
        res_fraction = self.get_dataset().get_attribute("fraction_residential_land")
        return ln_bounded(res_fraction/(1-res_fraction))
        