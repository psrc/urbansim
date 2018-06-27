# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array
from opus_core.variables.variable import Variable

class fraction_of_jobs_of_lum_sector_DDD_static(Variable):
    """ Fraction of jobs of sector DDD in buildings taken from the base year. Only non-residential buildings are considered in the static distribution"""
    _return_type="float32"
    
    sector_building_type_distribution = {
        #         0      1      2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17     18     19     20     21     22     23
    1: array([  0.00,  7.43,  1.48,  7.91,  0.00,  0.75,  0.03,  0.00, 12.41,  0.00,  1.45,  0.00,  0.00, 26.50,  0.00,  2.90,  5.61,  1.45,  0.30,  4.32,  0.63, 28.43,  0.30,  2.41,   ]),  
    2: array([  0.00,  0.28,  1.00,  8.77,  0.00,  0.45,  0.10,  0.03, 14.35,  0.00,  1.84,  0.00,  0.00, 32.46,  0.00,  0.07,  2.73,  0.33,  0.47,  2.69,  0.28, 34.84,  0.35,  1.65,   ]),  
    3: array([  0.00,  0.09,  0.17,  2.08,  0.00,  0.63,  0.02,  0.02, 47.05,  0.00,  0.37,  0.00,  0.00, 23.15,  0.00,  0.02,  0.16,  0.38,  0.06,  0.11,  0.15, 24.42,  0.06,  1.17,   ]),  
    4: array([  0.00,  0.04,  0.31,  7.59,  0.00,  0.93,  0.01,  0.00, 12.13,  0.00,  1.08,  0.00,  0.00, 27.72,  0.00,  0.12,  0.98,  0.15,  0.21,  0.36,  0.11, 46.59,  0.04,  1.97,   ]),  
    5: array([  0.00,  0.14,  1.17, 65.05,  0.00,  0.87,  0.05,  0.02,  2.01,  0.00,  2.00,  0.00,  0.00, 15.41,  0.00,  0.03,  1.13,  0.66,  0.08,  0.18,  0.02,  8.39,  0.35,  2.63,   ]),  
    7: array([  0.00,  0.07,  1.82, 10.56,  0.00,  0.22,  0.24,  0.05,  2.80,  0.00,  2.72,  0.00,  0.00, 70.32,  0.00,  0.05,  2.49,  0.62,  0.31,  0.78,  0.08,  6.90,  0.15,  0.60,   ]),  
    8: array([  0.00,  0.02,  2.10,  8.09,  0.00,  0.94,  4.79,  0.02,  1.18,  0.36,  3.28,  0.00,  0.00, 24.54,  0.00,  0.01,  0.63, 12.21, 35.46,  0.90,  0.32,  5.14,  0.25,  0.66,   ]),  
    9: array([  0.00,  0.30,  2.85,  6.71,  0.00,  1.12,  2.76,  15.56,  0.99,  0.02,  2.36,  0.00,  0.00, 55.04,  0.00,  0.06,  3.45,  0.81,  2.87,  0.65,  0.06,  3.21,  0.12,  1.73,   ]),  
    10: array([  0.00,  0.04,  1.49, 71.40,  0.00,  0.49,  0.25,  0.08,  2.10,  0.00,  5.80,  0.00,  0.00,  9.99,  0.00,  0.05,  1.65,  1.03,  0.43,  0.08,  0.01,  3.15,  0.23,  1.83,   ]),  
    11: array([  0.00,  0.25,  4.54, 42.55,  0.00,  2.18,  0.55,  0.08,  3.81,  0.02,  4.32,  0.00,  0.00, 16.96,  0.00,  0.43,  3.45,  7.89,  1.70,  1.08,  0.07,  7.55,  2.14,  1.51,   ]),  
    12: array([  0.00,  0.81,  1.27,  7.35,  0.00, 19.57,  0.17,  0.22,  2.38,  0.22,  0.59,  0.00,  0.00, 48.24,  0.00,  0.10,  1.23,  1.62,  2.57,  0.01,  0.66,  8.14,  3.40,  1.45,   ]),  
    13: array([  0.00,  0.05,  0.49,  0.58,  0.00,  1.41,  0.17,  0.12,  0.21,  0.00,  0.01,  0.00,  0.00,  2.41,  0.00,  0.21,  0.01,  2.88, 87.99,  0.01,  0.00,  2.36,  0.21,  0.87,   ]),  
                                       }
    
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["building.building_type_id"]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        distr = self.sector_building_type_distribution[self.sector_id]/100.
        return distr[ds["building_type_id"]]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.building.fraction_of_jobs_of_sector_9_static"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
  
        storage.write_table(
                 table_name='buildings',
                 table_data={
                    'building_id':       array([1, 2, 3, 4, 5, 6, 7]),
                    'building_type_id':  array([3, 22, 3, 5, 13, 13, 8])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        buildings = dataset_pool.get_dataset('building')
        
        values = buildings.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        #should_be = array([21.1, 0, 21.1, 1.2, 40.4, 40.4, 2.3 ])/100.0
        #self.assert_(ma.allclose(values, should_be),
        #    'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()