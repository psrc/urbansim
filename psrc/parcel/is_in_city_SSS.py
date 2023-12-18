# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, array

class is_in_city_SSS(Variable):
    """Returns a boolean indicating if the parcel is in city SSS (defined in cities table)"""
    
    def __init__(self, city_name):
        self.city_name = city_name
        Variable.__init__(self)
    
    def dependencies(self):
        return ["psrc.parcel.grid_id",
                "psrc.gridcell.city_id",
                "city.city_id",
                "city.city_name",                
                ]

    def compute(self, dataset_pool):
        cities = dataset_pool.get_dataset("city")
        city_names = array([city_name.lower() for city_name in cities.get_attribute("city_name")])
        matched_city_id = cities.get_attribute("city_id")[where(city_names == self.city_name.lower())]
        assert matched_city_id.size==1, "city name %s doesn't match to 1 unique city id" % self.city_name

        gridcells = dataset_pool.get_dataset("gridcell")
        city_id = self.get_dataset().get_join_data(gridcells, "city_id", "grid_id")
        return city_id == matched_city_id

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import ma
from psrc.datasets.parcel_dataset import ParcelDataset
from psrc.datasets.city_dataset import CityDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.parcel.is_in_city_seattle"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        parcels_table_name = 'parcels'
        
        storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'grid_id':array([1, 2, 1, 4, 3])
                    },
            )

        parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)        
        
        city_storage = StorageFactory().get_storage('dict_storage')
        
        cities_table_name = 'cities'
        
        city_storage.write_table(
                table_name=cities_table_name,
                table_data={
                    'city_id':array([63000, 56000, 99999]),
                    'city_name':array(["seattle", "bellevue", "skykomish"])
                    },
            )

        cities = CityDataset(in_storage=city_storage, in_table_name=cities_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, 
            data_dictionary = {
                'parcel':parcels,
                'city':cities,
                'gridcell':{
                            'grid_id':array([1,     2,     3, 4]),
                            'city_id':array([63000, 56000, 0, 63000])}
                }, 
            dataset = 'parcel'
            )
            
        should_be = array([True, False, True, True, False])
        
        self.assertTrue(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()