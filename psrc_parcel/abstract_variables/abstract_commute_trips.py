# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from numpy import zeros, logical_and

class abstract_commute_trips(Variable):
    """
    """
    origin_person_variable = "to_be_defined_in_fully_qualified_name"    
    destination_person_variable = "to_be_defined_in_fully_qualified_name"
     
    def dependencies(self):
        return [self.origin_person_variable,
                self.destination_person_variable
                ]

    def compute(self,  dataset_pool):
        dc = self.get_dataset()
        results = zeros(dc.size(), dtype='int32')
        
        persons = dataset_pool.get_dataset("person")
        home_district_id = persons.get_attribute(VariableName(self.origin_person_variable).get_alias())
        destination_district_id = persons.get_attribute(VariableName(self.destination_person_variable).get_alias())
        origin_array = dc.get_attribute("origin_district_id")
        distination_array = dc.get_attribute("destination_district_id")
        
        for i in range(dc.size()):
            results[i] = logical_and(home_district_id==origin_array[i], 
                                     destination_district_id==distination_array[i]).sum()
        return results
