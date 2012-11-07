# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros
from opus_core.simulation_state import SimulationState

class year(Variable):
    """"""
    def dependencies(self):
        return []

    def compute(self, dataset_pool):
        current_year = SimulationState().get_current_time()
        dataset = self.get_dataset()
        year = zeros( dataset.size(), dtype='i4' ) + current_year
        return year
