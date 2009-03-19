# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class is_in_employment_sector_DDD_industrial(Variable):
    """Is the job in employment_sector_DDD and industrial. """
    
    def __init__(self, number):
        self.tnumber = number
        self.is_in_sector = "is_in_employment_sector_" + str(self.tnumber)
        Variable.__init__(self)
        
    def dependencies(self):
        return [my_attribute_label(self.is_in_sector), 
                my_attribute_label("is_industrial")]
        
    def compute(self, dataset_pool):
        return logical_and(self.get_dataset().get_attribute(self.is_in_sector), 
                           self.get_dataset().get_attribute("is_industrial"))

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)
