# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
    
class is_building_use_SSS(Variable):
    """is building of building_use SSS (cie, med, mips, pdr, retail_ent, visitor)."""

    def __init__(self, building_use):
        self.building_use = building_use.lower()
        Variable.__init__(self)
        
    def dependencies(self):
        return ["building_use=building.disaggregate(building_use.building_use)"]
        
    def compute(self,  dataset_pool):
        name = self.get_dataset().get_attribute('building_use')
        name = map(lambda x: x.lower(),name)
        return  array(name) == self.building_use

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'building':
            {"building_id":array([1,2,3,4,5]),
             "building_use_id":array([1,2,1,3,1]),
#             "building_use":  strarray.array(["CIE", "mips", "cie", "pdr", "cie"]),
             },
            'building_use':
            {"building_use_id":array([1,2,3]),
             "building_use":  array(["CIE", "mips", "pdr"]),
             },
           }
        )
        
        should_be = array([1, 0, 1, 0, 1])
        instance_name = 'sanfrancisco.building.is_building_use_cie'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()
