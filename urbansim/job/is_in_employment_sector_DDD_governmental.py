# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class is_in_employment_sector_DDD_governmental(Variable):
    """Is the job in employment_sector_DDD and industrial. """
    
    def __init__(self, number):
        self.tnumber = number
        self.is_in_sector = "is_in_employment_sector_" + str(self.tnumber)
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.is_in_sector), 
                my_attribute_label("is_governmental")]
        
    def compute(self, dataset_pool):
        return logical_and(self.get_dataset().get_attribute(self.is_in_sector), 
                           self.get_dataset().get_attribute("is_governmental"))

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
