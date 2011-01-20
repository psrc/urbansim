# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import logical_or

class is_workerDDD_work_place_in_county_DDD_if_has_the_worker(Variable):
    """return is worker DDD's work_place in county DDD"""

    _return_type="bool8"

    def __init__(self, number1, number2):
        self.worker = "worker" + str(number1)
        self.county = "is_work_place_in_county_" + str(number2)
        Variable.__init__(self)

    def dependencies(self):
        return ["psrc.person.household_id",
                "psrc.person." + self.county,
                "psrc.person." + self.worker,
                attribute_label("household","household_id"),
                "psrc.household.has_" + self.worker,]
#                "%s = person.disaggregate(psrc.household.has_%s)" % (self.worker, self.worker)]

    def compute(self, dataset_pool):
        households = self.get_dataset()
        has_workerddd = households.get_attribute("has_" + self.worker)

        persons = dataset_pool.get_dataset('person')
        var_names = persons.get_attribute(self.county)
        is_workerddd = persons.get_attribute(self.worker)
        data = var_names * is_workerddd
        household_ids = persons.get_attribute("household_id")
        return logical_or(households.sum_over_ids(household_ids, data.astype("int8")),
                          (1 - has_workerddd))


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from opus_core.resources import Resources
from psrc.datasets.person_dataset import PersonDataset
from psrc.datasets.parcel_dataset import ParcelDataset
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.is_worker1_work_place_in_county_033_if_has_the_worker"

    def test_my_inputs(self):
        persons_storage = StorageFactory().get_storage('dict_storage')
        persons_table_name = 'persons'
        persons_storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5, 6]),
                    'household_id':array([1, 1, 2, 3, 3, 3]),
                    'member_id':array([1, 2, 1, 1, 2, 3]),
                    'worker1':array([1, 0, 0, 0, 0, 1]),
                    'work_place_parcel_id':array([1, 2, 3, 5, 4, 4])
                    },
            )
        persons = PersonDataset(in_storage=persons_storage, in_table_name=persons_table_name)

        parcels_storage = StorageFactory().get_storage('dict_storage')
        parcels_table_name = 'parcels'
        parcels_storage.write_table(
                table_name=parcels_table_name,
                table_data={
                    'parcel_id':array([1,2,3,4,5]),
                    'county':array(['033','061','035','033','033'])
                    },
            )
        parcels = ParcelDataset(in_storage=parcels_storage, in_table_name=parcels_table_name)

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'person':persons,
                'household':{
                    'household_id':array([1, 2, 3])
                    },
                'parcel':parcels
                },
            dataset = 'household'
            )
        should_be = array([1, 1, 1])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()