# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from numpy import array, where, zeros, nonzero
from opus_core.variables.variable import Variable
from opus_core.logger import logger
from .variable_functions import my_attribute_label

class annual_construction_schedule(Variable):
    """
    Returns the annual_construction_schedule depending on the number of units_proposed.
    """
    
    def dependencies(self):
        return [
                my_attribute_label("units_proposed"),
                "velocity_functions = velocity_function.annual_construction_schedule",
                "minimum_units = velocity_function.minimum_units",
                "maximum_units = velocity_function.maximum_units"
                ]
        
    def compute(self, dataset_pool):
        # get datasets
        development_project_proposal_components_dataset = self.get_dataset()
        velocity_functions_dataset = dataset_pool.get_dataset('velocity_function')
        
        # get attributes
        units_proposed = development_project_proposal_components_dataset.get_attribute('units_proposed')
        component_building_type_id = development_project_proposal_components_dataset.get_attribute('building_type_id')
        velocities = velocity_functions_dataset.get_attribute('annual_construction_schedule')
        velocity_building_type_id = velocity_functions_dataset.get_attribute('building_type_id')
        minimums = velocity_functions_dataset.get_attribute('minimum_units')
        maximums = velocity_functions_dataset.get_attribute('maximum_units')
        
        def get_longest_construction_schedule(building_type_id):
            btype = where(building_type_id==velocity_building_type_id, True, False)
            btypelen = zeros(btype.size, dtype=minimums.dtype)
            for i in btype.nonzero()[0]:
                btypelen[i] = len(eval(velocities[i]))
            max = btypelen.max()
            maxidx = where(btypelen==max)[0][0]
            longest_construction_schedule = velocities[maxidx]
            return longest_construction_schedule                
        
        def get_construction_schedule(building_type_id, units_proposed):
            min = where(units_proposed>=minimums, True, False)
            #TODO: CREATE A MAXIMUM -1 STYLE "I DONT CARE HOW HIGH" NUMBER
            max = where(units_proposed<=maximums, True, False)
            btype = where(building_type_id==velocity_building_type_id, True, False)
            construction_schedule_idx = (min==True) & (max==True) & (btype==True)
            if construction_schedule_idx.nonzero()[0].size > 1:
                #logger.log_warning("The number of proposed units for this proposal component falls")
                #logger.log_warning("within more than one range given in the velocity_functions dataset.")
                #logger.log_warning("Using the longest available velocity curve for this building type.")
                construction_schedule = get_longest_construction_schedule(building_type_id)
            elif construction_schedule_idx.nonzero()[0].size < 1:
                #logger.log_warning("The number of proposed units for this proposal component does not")
                #logger.log_warning("fall within the ranges given in the velocity_functions dataset.")
                #logger.log_warning("Using the longest available velocity curve for this building type.")
                construction_schedule = get_longest_construction_schedule(building_type_id)
            else:
                construction_schedule = velocities[construction_schedule_idx][0]
            return construction_schedule
        
        # calculate variable
        result = zeros(units_proposed.size, dtype=velocities.dtype)
        for i in range(0,units_proposed.size):
            cbtype_id = component_building_type_id[i]
            uproposed = units_proposed[i]
            csched = get_construction_schedule(cbtype_id, uproposed)
            result[i] = csched
        return result
    
from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_project_proposal_component':
            {
                 "proposal_component_id": arange(8)+1,
                 "building_type_id":      array([1, 1, 1, 1, 1, 1, 1, 1]),
                 "units_proposed":        array([0, 1, 2, 3, 4, 5, 6, 8])
             },
            'velocity_function':
            {
                 "velocity_function_id": arange(3)+1,
                 "annual_construction_schedule": array(["[100]", "[50, 100]", "[50, 75, 100]"]),
                 "building_type_id": array([1, 1, 1]),
                 "minimum_units": array([0, 3, 6]),
                 "maximum_units": array([2, 5, 10])        
            }
        })

        should_be = array(['[100]', '[100]', '[100]', '[50, 100]', '[50, 100]', '[50, 100]', '[50, 75, 100]', '[50, 75, 100]'])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)
        
    def test_my_inputs2(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_project_proposal_component':
            {
                 "proposal_component_id": arange(8)+1,
                 "building_type_id":      array([1, 1, 1, 1, 2, 2, 2, 2]),
                 "units_proposed":        array([0, 1, 2, 3, 5, 15, 51, 999])
             },
            'velocity_function':
            {
                 "velocity_function_id": arange(6)+1,
                 "annual_construction_schedule": array(["[100]", "[50, 100]", "[50, 75, 100]", "[25, 50, 100]", "[25, 50, 75, 100]", "[20, 40, 60, 80, 100]"]),
                 "building_type_id": array([1, 1, 1, 2, 2, 2]),
                 "minimum_units": array([0, 3, 6, 0, 11, 51]),
                 "maximum_units": array([2, 5, 10, 10, 50, 1000])        
            }
        })

        should_be = array(['[100]', '[100]', '[100]', '[50, 100]', '[25, 50, 100]', '[25, 50, 75, 100]', '[20, 40, 60, 80, 100]', '[20, 40, 60, 80, 100]'])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()

