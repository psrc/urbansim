# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
import numpy

class abstract_aggregate_travel_data_variable(Variable):
    """ Aggregate a travel data attribute with ndimage function by origin or destination zone
    """
    
    fill_value = 0
    aggregate_function = 'sum'       #name of the numpy function to do the aggregate, e.g. sum, mean, 
    aggregate_zone_id = 'to_be_defined_in_fully_qualified_name'  
    aggregate_by_origin = True       #whether the aggregate_zone_id is origin zone
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'
    additional_dependencies = []     #additional dependencies

    def dependencies(self):
        return [self.aggregate_zone_id, self.travel_data_attribute] + \
                self.additional_dependencies
    
    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        aggregate_zones = dataset.get_attribute(self.aggregate_zone_id)
        
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.fill_value)
        f = getattr(numpy, self.aggregate_function)
        axis = 1      #aggregate by row
        if not self.aggregate_by_origin:
            axis = 0  #aggregate by column
            
        results = f(travel_data_attr_mat, axis=axis)[aggregate_zones]        
        return results

##unittest in child class