# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from numpy import clip, inf

class residential_absorption(Variable):
    """"""
    lower_bound = .10
    def dependencies(self):
        return ['bayarea.submarket.residential_units', 
                'bayarea.submarket.households', 
                'bayarea.submarket.residential_units_lag1',
                'bayarea.submarket.households_lag1',
                ]

    def compute(self, dataset_pool):
        submarket = self.get_dataset()
        taken_up = clip(submarket['households'] - submarket['households_lag1'], 0, inf) 
        vacant_units = clip(submarket['residential_units'] - submarket['households'], 0, inf)
        results = safe_array_divide( taken_up, vacant_units.astype('f') )
        results = clip(results, self.lower_bound, 1.0)

        return results

