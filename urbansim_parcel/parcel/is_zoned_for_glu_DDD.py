# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
import numpy as np

class is_zoned_for_glu_DDD(Variable):
    
    def __init__(self, generic_land_use_type):
        Variable.__init__(self)
        self.glu = generic_land_use_type
        
    def compute(self,  dataset_pool):
        parcels = self.get_dataset()
        constraints = dataset_pool.get_dataset("development_constraint")         
        plan_types_for_glu = np.unique(constraints["plan_type_id"][np.logical_and(constraints["plan_type_id"] > 0,
                                                                                  np.logical_and(constraints["generic_land_use_type_id"] ==  self.glu,
                                                                                                 constraints["maximum"] > 0))])
        return np.in1d(parcels["plan_type_id"], plan_types_for_glu)
