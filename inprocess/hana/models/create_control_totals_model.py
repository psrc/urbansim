from random import sample 
from opus_core.models.model import Model
from opus_core.logger import logger
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import Dataset

class CreateControlTotalsModel(Model):
    model_name = 'Create Control Totals Model'
    
    def run(self, ct_directory, storage_type = 'csv_storage', in_table_prefix = "control_totals_", sample_range = None,
            dataset_name = "annual_household_control_total", dataset_pool = None, **kwargs):
        #sc = SessionConfiguration()
        existing_ct = dataset_pool.get_dataset(dataset_name, dataset_arguments={"id_name": []})
        ctstorage = StorageFactory().get_storage(storage_type, storage_location = ct_directory)
        if sample_range is not None:
            rn = sample(range(sample_range[0], sample_range[1]), 1)[0]
        else:
            rn = ''
        in_table_name = "%s%s" % (in_table_prefix, rn)
        kwargs.update({'in_storage':ctstorage, 'in_table_name': in_table_name})
        try:
            ct_dataset = DatasetFactory().search_for_dataset(dataset_name, dataset_pool.get_package_order(), arguments=kwargs)
        except: # take generic dataset
            ct_dataset = Dataset(dataset_name=dataset_name, **kwargs)
        # write values into the cache 
        ct_dataset.load_dataset()
        dataset_pool._remove_dataset(dataset_name)
        ct_dataset.write_dataset(out_storage=dataset_pool.get_storage(),
                                 out_table_name=existing_ct.resources["in_table_name"])
        ct = dataset_pool.get_dataset(dataset_name, dataset_arguments={"id_name": []})
        return ct

            

from opus_core.tests import opus_unittest
from opus_core.misc import ismember
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.resources import Resources
from numpy import array, logical_and, int32, int8, ma, all, allclose, arange

class Tests(opus_unittest.OpusTestCase):
                
    def test_sampling_ct(self):
        """ 
        """
        annual_household_control_totals_data = {
            "year": array([2000, 2000, 2000, 2000]),
            "age_of_head_min": array([ 50,  0,  50,  0]),
            "age_of_head_max": array([100, 49, 100, 49]),
            "persons_min":     array([  1,  1,   3,  3]),
            "persons_max":     array([  2,  2,   6,  6]),
            "total_number_of_households": array([16000, 26000, 16000, 26000])
            }

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='annual_household_control_totals', table_data=annual_household_control_totals_data)
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'], storage = storage)
        model = CreateControlTotalsModel()
        model.run(ct_directory = "/Users/hana/opus/urbansim_data/data/psrc_parcel/BMforTM/run_val2018_census_block_group/control_totals",
                  sample_range = [1,101], dataset_pool = dataset_pool, id_name = [])

if __name__=='__main__':
    opus_unittest.main()