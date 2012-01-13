# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded

class ln_emp_ratio(Variable):
    """Natural log of the inc for this gridcell"""
        
    _return_type="float32"

    def dependencies(self):
        return [
               "lnemp=ln_bounded(establishment.employment)",
               "lnemp_pre2=ln_bounded(establishment.employment_lag2)",
               ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        result = dataset['lnemp'] - dataset['lnemp_pre2']
        return result
