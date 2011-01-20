# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
from numpy import zeros, dot, newaxis, array
try:
    import networkx as nx
except ImportError:
    nx = None

class mean_income_kDDD(Variable):
    """mean income for DDD order expansion
    Used in GNSI (Generalized Neighborhood Sorting Index) (Jargowsky and Kim, 2005) :
    GNSI^2 = numpy.sqrt( alldata.aggregate_all( zone.number_of_agents(household) * numpy.square(sanfrancisco.zone.mean_income_k2 - zone.aggregate_all(household.income, function=mean)) ) / alldata.aggregate_all( numpy.square(household.income - household.aggregate_all(household.income, function=mean)) )) 
    """

    _return_type = "float32"
    
    def __init__(self, order):
        self.order = order
        Variable.__init__(self)
    
    def dependencies(self):
        return ["sum_income=zone.aggregate(household.income)",
                "sum_households=zone.number_of_agents(household)",
                "adjacent_zone.zone_id",
                "adjacent_zone.adjacent_zone_id"
                ]

    def compute(self,  dataset_pool):
        """ use networkx to determine whether two geographies are adjacent with
        k degree of expansion
        """

        zones = self.get_dataset()
        adjacent_zones = dataset_pool.get_dataset('adjacent_zone')
        id_max = zones['zone_id'].max()+1
        W = zeros((id_max, id_max), dtype='int8')  #diagonal
        
        sum_income = zeros(id_max, dtype=zones['sum_income'].dtype)
        sum_households = zeros(id_max, dtype=zones['sum_households'].dtype)
        sum_income[zones['zone_id']] = zones['sum_income']
        sum_households[zones['zone_id']] = zones['sum_households']
        if not nx: raise ImportError, "networkx module is required."
        G = nx.Graph()
        G.add_nodes_from(zones['zone_id'])
        G.add_edges_from(adjacent_zones.get_multiple_attributes(['zone_id', 'adjacent_zone_id']))
        length = nx.all_pairs_shortest_path_length(G, cutoff=self.order)
        
        for key, val in length.items():
            W[key][val.keys()] = 1
        
        sum_income = dot(W, sum_income[:, newaxis])[:, 0]
        sum_households = dot(W, sum_households[:, newaxis])[:, 0]

        results = safe_array_divide(sum_income, sum_households.astype('f'))
        return results[zones['zone_id']]
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    """
    """
    def test_my_inputs(self):
        """ test k=0,1,2
        """
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'household':
            {"household_id": array([ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
             "zone_id":      array([ 1, 1, 2, 2, 3, 3, 4, 2, 1, 3]),
             "income":       array([ 0,10,45,30,20,50,85,21,20,65])*1000,
            },
            'zone':
            {
             "zone_id":  array([1,2,3,4]),
             },
            'adjacent_zone':
            {
             #  1 | 2  
             #  - - -
             #  3 | 4
             "zone_id":           array([1,1,2,2,3,3,4,4]),
             "adjacent_zone_id":  array([2,3,1,4,1,4,2,3]),
             },
             
           }
        )
        
        instance_name = 'sanfrancisco.zone.mean_income_k0'
        should_be = array([10, 32, 45, 85])*1000 
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

        instance_name = 'sanfrancisco.zone.mean_income_k1'
        should_be = array([29, 30.142857, 35.714285, 45.142857])*1000
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

        instance_name = 'sanfrancisco.zone.mean_income_k2'
        should_be = array([34.6, 34.6, 34.6, 34.6])*1000
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__ == '__main__':
    if nx:
        opus_unittest.main()
