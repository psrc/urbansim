# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
    
class has_DDD_workers(Variable):
    """if a household has DDD workers"""

    def __init__(self, nworkers):
        self.nworkers = nworkers
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_has_%s_workers = household.nfulltime==%s" % (self.nworkers, self.nworkers)
                ]
        
    def compute(self,  dataset_pool):
        return  self.get_dataset().get_attribute("_has_%s_workers" % self.nworkers )
