#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
from urbansim.functions import attribute_label
    
class number_of_workers_category(Variable):
    """break number of workers to category"""
        
    def dependencies(self):
        return ["household.nfulltime"
                ]
        
    def compute(self,  dataset_pool):
        hhs = self.get_dataset().get_attribute("nfulltime")
        results = zeros(hhs.size)      #by default, categorize to 0
        results[hhs==1] = 1            #change to 1 if household size is 1
        results[hhs==2] = 2            #change to 2 if household size is 2
        results[hhs>=3] = 3            #change to 2 if household size is 2        
        return results
