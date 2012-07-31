# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.simulation_state import SimulationState

class SSS_2010(Variable):
    """return zone attribute variable of 2010"""

    year = 2010

    def __init__(self, variable):
        self.variable = variable
        Variable.__init__(self)

    def dependencies(self):
        current_year = SimulationState().get_current_time()
        lag = current_year - self.year
        self.lag_name = '{}_lag{}'.format(self.variable, lag)
        return ['bayarea.zone.{}'.format(self.lag_name)]

    def compute(self, dataset_pool):
        return self.get_dataset()["{}".format(self.lag_name)]
         
