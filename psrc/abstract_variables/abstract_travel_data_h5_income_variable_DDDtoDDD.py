# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.misc import unique
from numpy import ones, where

class abstract_travel_data_h5_income_variable_DDDtoDDD(Variable):
    """ Abstract variable for travel model skims that use income groups.
        DDDtoDDD define from time and to time. If more than one time period is selected, 
        the skims are averaged over the time periods.
    """
    default_value = -1
    origin_zone_id = 'to_be_defined_in_fully_qualified_name'
    destination_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_short_name' # use 'INC' as income group mask
    income_groups_attribute = 'to_be_defined_in_fully_qualified_name'

    def __init__(self, from_time, to_time):
        self._from_time = from_time
        self._to_time = to_time
        Variable.__init__(self)

    def dependencies(self):
        return [ self.origin_zone_id, 
                self.destination_zone_id, self.income_groups_attribute,
                'travel_data_link.data_link']
    
    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        origin_zones = dataset.get_attribute(VariableName(self.origin_zone_id).get_alias())
        destination_zones = dataset.get_attribute(VariableName(self.destination_zone_id).get_alias())
        income_groups = dataset.get_attribute(VariableName(self.income_groups_attribute).get_alias())
        uincome_groups = unique(income_groups)
    
        travel_data_link = dataset_pool.get_dataset('travel_data_link')
        travel_data_h5 = travel_data_link.get_skim_dataset()
        
        result = self.default_value*ones(dataset.size()).astype('float32')
        for igroup in uincome_groups:
            index_income_group = where((income_groups==igroup)*(origin_zones > 0)*(destination_zones>0))[0]
            attr_name = self.travel_data_attribute.replace("INC", str(igroup))
            travel_data_attr = travel_data_h5.get_attribute(attr_name, 
                                            origin_zones[index_income_group], 
                                            destination_zones[index_income_group],
                                            from_time=self._from_time, to_time=self._to_time)
            result[index_income_group] = travel_data_attr.astype(result.dtype)
        return result

##unittest in child class
