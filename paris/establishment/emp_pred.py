# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
#paris.establishment.ln_emp_ratio*establishment.employment_lag2
from opus_core.variables.variable import Variable, ln_bounded
from numpy import clip

class emp_pred(Variable):
    """Natural log of the inc for this gridcell"""
        
    _return_type="int32"

    def dependencies(self):
        return [
               "paris.establishment.emp_ratio",
			   "emp_pre1=establishment.employment_lag1",
               ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        result = dataset['emp_ratio'] * dataset['emp_pre1']
        #result = clip(result, 0, 15000)
        return result
