# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros

class subtract_from_travel_data_SSS(Variable):
    """Attribute SSS is taken from zone-to-zone travel data and values on links that go from node to the zone centroids
        are subtracted. The attribute SSS has to be a primary attribute of the travel_data dataset and must be know to 
        the node_travel_data_dataset.
    """
    
    def __init__(self, attribute):
        self.attribute = attribute
        Variable.__init__(self)
        
    def dependencies(self):
        return ["travel_data.%s" % self.attribute, "psrc_parcel.node_travel_data.%s" % self.attribute]

    def compute(self,  dataset_pool):
        commutes = self.get_dataset()
        nodes = dataset_pool.get_dataset('node_travel_data')
        travel_data = dataset_pool.get_dataset('travel_data')
        attr_type = travel_data.get_attribute(self.attribute).dtype
        result = zeros(commutes.size(), dtype=attr_type)
        ids = commutes.get_id_attribute()
        for i in range(commutes.size()):
            #print "commute %s" % commutes.get_attribute('name')[i]
            from_node, to_node = ids[i]
            result[i] = commutes.get_attribute_from_travel_data(self.attribute, from_node, to_node, nodes, travel_data)
            #print "result = %s" % result[i]
        return result

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim_parcel', 'urbansim'],
            test_data={
                'travel_data':
                    { 'from_zone_id': array([1, 3, 1, 368, 416]),
                      'to_zone_id' :array( [ 2, 2, 3, 416, 368]),
                      'travel_time': array([ 150, 73, 230, 15.5, 17.2])
                     },
                'node_travel_data':
                    {
                     'from_node_id': array([2873, 1348, 1421, 4835, 6628, 6523, 10, 2189]),
                     'to_node_id':   array([1348, 1421, 1348, 6628, 6523, 6628, 15, 2190]),
                     'travel_time': array([ 1.1,   0.4,  0.9,  2.5,  3.6,   0.1, 8.7, 0.8])
                     },
                'commute_travel_data':
                    {
                     'from_node_id': array([2873, 4835, 10]),
                     'to_node_id':   array([4835, 2873, 20])
                     }
                    }
        )
        
        should_be = array([15.5-1.1-0.4-2.5-3.6, 17.2-1.1-0.4-2.5-3.6, 0])
        instance_name = 'psrc_parcel.commute_travel_data.subtract_from_travel_data_travel_time'
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()