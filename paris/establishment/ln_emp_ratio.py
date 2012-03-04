# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable, ln_bounded
from opus_core.simulation_state import SimulationState

class ln_emp_ratio(Variable):
    """"""
        
    _return_type="float32"
    base_year = 1999

    def dependencies(self):
        current_year = SimulationState().get_current_time()
        if current_year == self.base_year: #for estimation
            lag = 2
        else: #for simulation
            lag = 1

        return [
               "lnemp=ln_bounded(establishment.employment)",
               "lnemp_pre=ln_bounded(establishment.employment_lag%s)" % lag,
               ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        result = dataset['lnemp'] - dataset['lnemp_pre']
        return result
