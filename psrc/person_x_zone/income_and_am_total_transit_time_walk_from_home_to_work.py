# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class income_and_am_total_transit_time_walk_from_home_to_work(Variable):
    """ income * am_total_transit_time_walk_from_home_to_work"""
    _return_type="float32"
    travel_time = "am_total_transit_time_walk_from_home_to_work"
    hh_income = "income"
    
    def dependencies(self):
        return ["psrc.person_x_zone." + self.travel_time,
                attribute_label("person", self.hh_income)]

    def compute(self, dataset_pool):
#        parcel_ln_rbuilt_sf = ln(self.parcel_built_sf)
        person_x_zones = self.get_dataset()
        income = person_x_zones.get_dataset(1).get_attribute_by_index(self.hh_income, person_x_zones.get_2d_index_of_dataset1())
        travel_time = person_x_zones.get_attribute("am_total_transit_time_walk_from_home_to_work")
        return income * travel_time


from numpy import array
from numpy import ma

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person_x_zone.income_and_am_total_transit_time_walk_from_home_to_work"
    
    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage.write_table(
            table_name='persons',
            table_data={
                'person_id':array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 2, 3, 3, 3]),
                'member_id':array([1, 2, 1, 1, 2, 3]),
                'income': array([100, 300, 30, 200, 10, 30])
                },
        )
        storage.write_table(
            table_name='zones',
            table_data={
                'zone_id':array([1, 2, 3]),
                },
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id':array([1,2,3,4,5]),
                'zone_id':array([3, 1, 1, 1, 2]),
                },
        )
        storage.write_table(
            table_name='travel_data',
            table_data={
                'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                'to_zone_id':array([1,3,1,3,2,1,3,2,2]),
                'am_total_transit_time_walk':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['psrc', 'urbansim'],
                                   storage=storage)

        person_x_zone = dataset_pool.get_dataset('person_x_zone')
        person_x_zone.compute_variables(self.variable_name,
                                        dataset_pool=dataset_pool)
        values = person_x_zone.get_attribute(self.variable_name)
        
        should_be = array([[100*1.1, 100*7.8, 100*2.2], 
                           [300*1.1,300*7.8, 300*2.2], 
                           [30*3.3, 30*0.5, 30*4.4], 
                           [200*3.3, 200*0.5, 200*4.4],
                           [10*3.3, 10*0.5, 10*4.4], 
                           [30*3.3, 30*0.5, 30*4.4]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-3), 
                     msg="Error in " + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()