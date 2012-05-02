# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class sectorDDD_employment(Variable):
    """total number of employment of sectorDDD"""

    _return_type="int32"
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return [
                "is_sector{0}=establishment.sector_id=={0}".format(self.sector_id), 
                "not_disappeared = numpy.logical_not(establishment.disappeared)",
                "zone_id=establishment.disaggregate(building.zone_id)",
                "_emp{0}=zone.aggregate(establishment.is_sector{0} * establishment.not_disappeared)".format(self.sector_id)
                ]

    def compute(self,  dataset_pool):
        return self.get_dataset()['_emp{0}'.format(self.sector_id)]

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0")

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
            'establishment':
            {"establishment_id":array([1,2,3,4,5]),
            "zone_id":          array([1,1,2,2,2]),
             "sector_id":       array([2,2,1,1,2]),
             "disappeared":     array([0,0,1,0,1]),
             },
            'zone':
            {"zone_id":array([1,2]),
             },
           }
        )
        
        instance_name = 'paris.zone.sector1_employment'
        should_be = array([0, 1])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        instance_name = 'paris.zone.sector2_employment'
        should_be = array([2, 0])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
