# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class has_DDD_nonhome_based_workers(Variable):
    """return if a household has DDD nonhome based worker"""
    
    _return_type="bool8"

    def __init__(self, number):
        self.workers = number
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.household.number_of_nonhome_based_workers"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("number_of_nonhome_based_workers") == self.workers