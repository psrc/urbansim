# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import int32
from .variable_functions import my_attribute_label
from opus_core.logger import logger

try:
    import networkx
except:
    logger.log_warning('Could not load networkx. Skipping %s.' % __file__)
else:
    class travel_time_hbw_transit_from_work_to_home(Variable):
        """Transit travel time frome home to work.
        """
        default_value = 18000

        def dependencies(self):
            return [my_attribute_label("home_parcel_id"),
                    my_attribute_label("work_place_parcel_id"),
                    "transit_accessibility.edge.target",
                    ]

        def compute(self, dataset_pool):
            edges = dataset_pool.get_dataset('edge')
            edges.get_graph(create_using=networkx.XDiGraph(),edgetype=int)

            persons = self.get_dataset()
            homes = persons.get_attribute("home_parcel_id").astype(int32)
            workplaces = persons.get_attribute("work_place_parcel_id").astype(int32)
            pairs = list(map(lambda x,y: (x, y), workplaces, homes))
            results = edges.compute_dijkstra_path_length(pairs,
                                                         default_value=self.default_value)

            return results


    from opus_core.tests import opus_unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from psrc.datasets.person_dataset import PersonDataset
    from transit_accessibility.datasets.edge_dataset import EdgeDataset
    from opus_core.storage_factory import StorageFactory


    class TestsPersonTravelTimeHbwTransitFromWorkToHome(opus_unittest.OpusTestCase):
        variable_name = "transit_accessibility.person.travel_time_hbw_transit_from_work_to_home"

        def setUp(self):
            logger.enable_hidden_error_and_warning_words()

        def tearDown(self):
            logger.disable_hidden_error_and_warning_words()

        def test_my_inputs(self):
            storage = StorageFactory().get_storage('dict_storage')

            edges_table_name = 'edges'
            storage.write_table(
                    table_name=edges_table_name,
                    table_data={
                        'source':array([1,  2,   1,   3]),
                        'target':array([2,  3,   3,   1]),
                        'cost':array([12, 1, 15, 17])
                        },
                )

            persons_table_name = 'persons'
            storage.write_table(
                    table_name=persons_table_name,
                    table_data={
                        'person_id':array([1,2,3,4,5,6]),
                        'household_id':array([1,1,3,3,4,5]),
                        'member_id':array([1,2,1,2,4,1]),
                        'home_parcel_id':array([3, 1, 1, 2, 2, 3]),
                        'work_place_parcel_id':array([1, 3, 3, 1, 4, 2])
                        },
                )

            edges = EdgeDataset(in_storage=storage, in_table_name=edges_table_name)
            persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

            values = VariableTestToolbox().compute_variable(self.variable_name,
                data_dictionary = {
                    'person':persons,
                    'edge':edges
                    },
                dataset = 'person'
                )

            default_value = travel_time_hbw_transit_from_work_to_home.default_value
            should_be = array([13, 17, 17, 12, default_value, 1])

            values = [value[0] for value in values]

            self.assertTrue(ma.allclose(values, should_be, rtol=1e-3),
                'Error in ' + self.variable_name)


    if __name__=='__main__':
        opus_unittest.main()