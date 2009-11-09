# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, where, minimum
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class generalized_cost_hbw_am_drive_alone_to_bellevue_cbd(Variable):
    """Generalized cost for travel to the Bellevue CBD. It is the minimum of costs for travels to zones that have bellevue_cbd=1.
    The cost used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    _return_type = 'float32'

    def dependencies(self):
        return ['zone.bellevue_cbd']

    def compute(self, dataset_pool):
        zones = self.get_dataset()
        is_in_cbd = zones.get_attribute('bellevue_cbd')
        zones_in_cbd = zones.get_id_attribute()[where(is_in_cbd)]
        min_values = array(zones.size()*[2**30], dtype=self._return_type)
        for zone_id in zones_in_cbd:
            variable_name = my_attribute_label("generalized_cost_hbw_am_drive_alone_to_%s" % zone_id)
            self.add_and_solve_dependencies([variable_name], dataset_pool=dataset_pool)
            min_values = minimum(min_values, zones.get_attribute(variable_name))
        min_within_cbd = min_values[where(is_in_cbd)].min()
        min_values[where(is_in_cbd)] = min_within_cbd
        return min_values
