# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from numpy import clip, inf

class non_residential_absorption(Variable):
    """"""
    lower_bound = .10
    upper_bound = 1.0
    def dependencies(self):
        return ['bayarea.employment_submarket.non_residential_sqft', 
                'bayarea.employment_submarket.occupied_non_residential_sqft', 
                'bayarea.employment_submarket.non_residential_sqft_lag1',
                'bayarea.employment_submarket.occupied_non_residential_sqft_lag1',
                ]

    def compute(self, dataset_pool):
        submarket = self.get_dataset()
        uptake = clip(submarket['occupied_non_residential_sqft'] - submarket['occupied_non_residential_sqft_lag1'], 0, inf) 
        vacant_units = clip(submarket['non_residential_sqft'] - submarket['occupied_non_residential_sqft'], 0, inf)
        results = safe_array_divide( uptake, vacant_units.astype('f') )
        results = clip(results, self.lower_bound, self.upper_bound)
        results[vacant_units==0] = self.upper_bound

        return results

