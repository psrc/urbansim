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

from random import choice

from opus_core.variables.variable import Variable
from numpy import array

class something_like_sum_demand(Variable):
    """A variable for unit tests.
    """ 
    _return_type="float32"
        
    def dependencies(self):
        return ['waterdemand.consumption_re.sum_demand']
        
    def compute(self, dataset_pool):
        sum_demand = self.get_dataset().get_attribute('sum_demand')
        values = []
        for num in sum_demand:
            values.append(num + choice([1,-1])*choice([.1, .1, .1, .1, .1, .2, .2, .2, .2, .3, .3, .3, .4, .4, .5])*num)
        return array(values)