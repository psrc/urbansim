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
from numpy import float32

class share_of_de_population_DDD(Variable):
    """share of population in the faz.
"""
    _return_type="float32"

    def __init__(self, number):
        self.tnumber = number
        self.variable_name = "de_population_" + str(int(number))
        Variable.__init__(self)
    
    
    def dependencies(self):
        return [attribute_label("faz", self.variable_name)]
    
    def compute(self, dataset_pool):
        population = self.get_dataset().get_attribute(self.variable_name)
        return population.astype(float32) / population.sum()
