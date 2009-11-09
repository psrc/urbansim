# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class absolute_SSS_difference_from_baseline(Variable):
    """difference of variable SSS from baseline_SSS"""

    def __init__(self, variable_name):
        self.variable_name = variable_name
        Variable.__init__(self)
    
    def dependencies(self):
        #resource and construction sectors are hard-coded as sector 1 and 2
        return ["urbansim.gridcell." + self.variable_name,
                my_attribute_label("baseline_%s" % self.variable_name)]

    def compute(self, dataset_pool):
        gridcells = self.get_dataset()
        return gridcells.get_attribute(self.variable_name) - \
               gridcells.get_attribute("baseline_%s" % self.variable_name) 
