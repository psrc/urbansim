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
from urbansim.functions import attribute_label

class abstract_sum_from_gridcells(Variable):
    """Sum of any variable over zones.
"""
    gc_variable = "not_defined"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_variable), 
                 attribute_label("gridcell", "zone_id")]
    
    def compute(self, dataset_pool):
        return self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'), self.gc_variable)
