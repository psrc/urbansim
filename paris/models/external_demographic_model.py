# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.models.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger
from numpy import ones, in1d, array, allclose, sort
from pandas import HDFStore, DataFrame

class ExternalDemographicModel(Model):
    """ A model that updates households with external demographic data; 
        it replaces household transition model
    """
    model_name = "External Demographic Model"

    def __init__(self, model_name=None, model_short_name=None):
        """
        model_name: optional
        model_short_name: optional
        """
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name

    def run(self, demographic_data_file, 
            household_dataset, 
            year=None,
            keep_attributes=None,
            fill_value=-1,
            demographic_attributes=None,
            dataset_pool=None
            ): 
        """
        demographic_data_file: an hdf5 file that contains households and persons data
                               in pandas DataFrame format.  
                               Run paris/scripts/prepare_demographic_data.py to create
                               the file.
        household_dataset: opus dataset of household
        year: integer, optional
        keep_attributes: list, attributes to keep from household dataset
        fill_value: fill attributes with fill_value for new households
        demographic_attributes: dictionary, attributes to load from external
                                demographic file.  The key of the dictionary is 
                                attribute name for household data, its value is
                                the expression to compute the attribute value.
                                See unittest for example.
        dataset_pool: opus DatasetPool object, optional
        """
        hh_ds = household_dataset
        if year is None:
            year = SimulationState().get_current_time()
        ## this relies on the order of household_id in
        ## households data and persons attributes summarized 
        ## by household_id is the same
        dmgh_data = HDFStore(demographic_data_file)
        households = dmgh_data['households'].ix[year]
        persons = dmgh_data['persons'].ix[year]
        n_hhs = len(households)
        hh_ids = sort(households.index.values)
        results = {}
        results['household_id'] = hh_ids
        for k, v in demographic_attributes.iteritems():
            results[k] = eval(v)
            results[k] = results[k][hh_ids].values
            assert results[k].size == n_hhs

        logger.log_status( ('Loaded demographic characteristics %s for %s ' +\
                          'households from external file %s.') % \
                           ( demographic_attributes.keys(), 
                            n_hhs, 
                            demographic_data_file) )

        is_existing = in1d(hh_ids, hh_ds['household_id'])
        for attr in keep_attributes:
            dtype = hh_ds[attr].dtype
            values = fill_value * ones(n_hhs, dtype=dtype)
            values[is_existing] = hh_ds.get_attribute_by_id(attr,
                                                            hh_ids[is_existing])
            results[attr] = values

        storage = StorageFactory().get_storage('dict_storage')

        table_name = 'households'
        storage.write_table(table_name=table_name,
                            table_data=results)

        new_hh_ds = Dataset(in_storage=storage, 
                            in_table_name=table_name,
                            id_name=household_dataset.get_id_name(),
                            dataset_name=household_dataset.dataset_name)
        household_dataset = new_hh_ds
        if dataset_pool is not None:
            dataset_pool.replace_dataset(household_dataset.dataset_name,
                                         household_dataset)
        return household_dataset

import os        
import tempfile
import shutil
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class Tests(opus_unittest.OpusTestCase):
    """unittest"""        
    def setUp(self, attribute_cache=True):
        hh_data = {
            'household_id':  array([1,   2,  3,  4]),
            'building_id':   array([11, 22, 33, 22]),
            'size':          array([4,   3,  2,  1]),
            'income':        array([51, 52, 53, 54])*1000,
            'keep':          array([4.1, 4.2, 4.3, 4.4]),
            }
        if attribute_cache:
            self.tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')
            SimulationState().set_cache_directory(self.tmp_dir)
            self.attribute_cache = AttributeCache()
            self.dataset_pool = SessionConfiguration(new_instance=True,
                                     package_order=['urbansim', 'opus_core'],
                                     in_storage=self.attribute_cache
                                    ).get_dataset_pool()        

            self.attribute_cache.write_table(table_name='households', 
                                             table_data=hh_data)
            self.hh_ds = self.dataset_pool.get_dataset('household')
        else:
            storage = StorageFactory().get_storage('dict_storage')
            table_name = 'households'
            storage.write_table(table_name=table_name,
                                table_data=hh_data)

            self.hh_ds = Dataset(in_storage=storage, 
                                     in_table_name=table_name,
                                     dataset_name='household')

        self.dmgh_data_dir = tempfile.mkdtemp(prefix='urbansim_tmp')
        self.dmgh_data_file = os.path.join(self.dmgh_data_dir, 
                                           'demographic_data.h5')
        store = HDFStore(self.dmgh_data_file)
        ## order should not matter
        hh = {
            'year':         array([ 0, 0, 0, 0, 1])+2000,
            'household_id': array([ 5, 1, 2, 3, 1]),
            'income':       array([65,61,62,63,71])*1000,
        }
        ps = {
            'year':         array([0, 0, 0, 0, 0, 0, 0, 0, 
                                   0, 0, 0, 1, 1, 1, 1, 1])+2000,
            'person_id':    array([1, 2, 3, 4, 5, 6, 9,10, 
                                   7, 8,81, 1, 2, 3, 4, 31]),
            'household_id': array([1, 1, 1, 2, 2, 2, 5, 5, 
                                   3, 3, 3, 1, 1, 1, 1, 1]),
        }
        hh = DataFrame(hh) 
        hh.set_index(['year', 'household_id'], inplace=True)
        ps = DataFrame(ps)
        ps.set_index(['year', 'person_id'], inplace=True)
        store['households'] = hh
        store['persons'] = ps
        store.close()

    def tearDown(self):
        shutil.rmtree(self.dmgh_data_dir)        
        if hasattr(self, 'tmp_dir'):
            shutil.rmtree(self.tmp_dir)        

    def test_run1(self):
        model = ExternalDemographicModel()
        new_hh_ds = model.run(self.dmgh_data_file, self.hh_ds,
                  year=2000, 
                  keep_attributes=['building_id', 'keep'],
                  demographic_attributes={'income': "households.income",
                          'size'  : "persons.groupby('household_id').size()" }
                 )

        assert allclose(new_hh_ds['household_id'], array([ 1,  2,  3,  5]))
        assert allclose(new_hh_ds['building_id'],  array([11, 22, 33, -1]))
        assert allclose(new_hh_ds['keep'],         array([4.1, 4.2, 4.3, -1]))
        assert allclose(new_hh_ds['income'],       array([61, 62, 63, 65])*1000)
        assert allclose(new_hh_ds['size'],         array([ 3,  3,  3,  2]))
        
if __name__ == '__main__':
    opus_unittest.main()
