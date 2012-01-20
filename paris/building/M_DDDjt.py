# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from opus_core.simulation_state import SimulationState
from numpy import ma

class M_DDDjt(Variable):
    """"""
    base_year = 1999
    def __init__(self, type_id):
        self.type_id = type_id
        Variable.__init__(self)
 
    def dependencies(self):
        current_year = SimulationState().get_current_time()
        lag = current_year - self.base_year
        
        return [
                "M_hij0 = paris.building.number_of_households_of_type_{0}_lag{1}".format(self.type_id, lag),
                "TM_hit = alldata.aggregate_all(numpy.logical_and(household.hh_type=={0}, household.building_id<=0))".format(self.type_id),
                "TM_hi0 = paris.alldata.number_of_households_of_type_{0}_lag{1}".format(self.type_id, lag),
                "V_ijt = urbansim_zone.building.vacant_residential_units",
                "V_ij0 = urbansim_zone.building.vacant_residential_units_lag{}".format(lag),
                
                ]

    def compute(self, dataset_pool):
        import ipdb; ipdb.set_trace()
        ds = self.get_dataset()
        alldata = dataset_pool.get_dataset('alldata')
        results = ds['M_hij0'] * safe_array_divide(alldata['TM_hit'], alldata['TM_hi0']) * safe_array_divide(ds['V_ijt'], ds['V_ij0'])
        return results


