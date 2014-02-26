# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import zeros, float32, indices, repeat, arange, tile
from opus_core.storage_factory import StorageFactory
import os

from opus_emme2.travel_model_output import TravelModelOutput as ParentTravelModelOutput

class TravelModelOutput(ParentTravelModelOutput):
    """
    A class to access the output of emme4 travel models in any format (e.g. hdf5 or directly from memory).
    """

    def get_travel_data_set(self, zone_set, matrix_attribute_name_map, 
                            out_storage=None, **kwargs):
        """
        Returns a new travel data set containing the given set of emme matrices 
        populated from given storage. The columns in the travel data set are 
        those given in the attribute name of the map.
        """
        # Compute the from and to zone sets
        nzones = zone_set.size()
        comb_index = indices((nzones,nzones))
                                       
        table_name = 'storage'
        in_storage = StorageFactory().get_storage('dict_storage')
        in_storage.write_table(
                table_name=table_name,
                table_data={
                    'from_zone_id':zone_set.get_id_attribute()[comb_index[0].ravel()].astype('int32'),
                    'to_zone_id':zone_set.get_id_attribute()[comb_index[1].ravel()].astype('int32'),
                    }
            )
                                       
        travel_data_set = TravelDataDataset(in_storage=in_storage, 
            in_table_name=table_name, out_storage=out_storage)
        travel_data_set.load_dataset_if_not_loaded()
        max_zone_id = zone_set.get_id_attribute().max()

        for matrix_name in matrix_attribute_name_map.keys():
            self._put_one_matrix_into_travel_data_set(travel_data_set, max_zone_id, matrix_name, 
                                                     matrix_attribute_name_map[matrix_name], **kwargs)
        return travel_data_set

            
    def _put_one_matrix_into_travel_data_set(self, travel_data_set, max_zone_id, matrix_name, 
                                            attribute_name, table_name, in_storage):
        """
        Adds to the given travel_data_set the data for the given matrix.
        """
        logger.start_block('Copying data for matrix %s into variable %s' %
                           (matrix_name, attribute_name))
        try:
            attr = in_storage.load_table(table_name,column_names=[matrix_name])
                      
            travel_data_set.add_primary_attribute(data=zeros(travel_data_set.size(), dtype=float32), 
                                                  name=attribute_name)
            if attr[matrix_name].size == 0:
                logger.log_error("Skipped exporting travel_data attribute %s: No data is exported from EMME matrix." % attribute_name)
            else:
                nzones = attr[matrix_name].shape[0]
                zones = arange(1,nzones+1)
                Ozones = repeat(zones, nzones)
                Dzones = tile(zones, (nzones, 1)).flatten()
                travel_data_set.set_values_of_one_attribute_with_od_pairs(attribute=attribute_name,
                                                                          values=attr[matrix_name].flatten(),
                                                                          O=Ozones, D=Dzones)
        finally:
            logger.end_block()
            


from tempfile import mkdtemp
from shutil import rmtree
from numpy import array, ones, allclose
from opus_core.tests import opus_unittest
from opus_core.store.hdf5g_storage import hdf5g_storage

from urbansim.datasets.zone_dataset import ZoneDataset

class TravelModelOutputTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = mkdtemp(prefix='psrc_parcel_test_emme_skims')
        self.bank_file = os.path.join(self.temp_dir, '2015-travelmodel.h5')         
        self.bank_storage = hdf5g_storage(storage_location=self.bank_file)
        data = {
            'au1tim': array([[2,  5,  7],
                             [1.3,7.9,3],
                             [6,  10, 0]]),
            'biketm': array([[10,  50,  65],
                             [13, 10.9, 40],
                             [56,  100, 21]])
            }
        self.bank_storage.write_table(table_name = 'Bank1', table_data = data)
        zone_storage = StorageFactory().get_storage('dict_storage')
        zone_table_name = 'zone'
        zone_storage.write_table(
                    table_name=zone_table_name,
                    table_data={
                        'zone_id': array([1,2,3]),
                        'travel_time_to_airport': ones((3,)),
                        'travel_time_to_cbd': ones((3,))
                        },
                )
        self.zone_set = ZoneDataset(in_storage=zone_storage, in_table_name=zone_table_name)                 
        travel_data_storage = StorageFactory().get_storage('dict_storage')
        travel_data_table_name = 'travel_data'
        travel_data_storage.write_table(
                    table_name=travel_data_table_name,
                    table_data={
                        'from_zone_id':array([1,1,1,2,2,2,3,3,3]),
                        'to_zone_id':array([  1,2,3,3,2,1,1,2,3]),
                        },
        )
            
        self.travel_data_set = TravelDataDataset(in_storage=travel_data_storage, in_table_name=travel_data_table_name)

         
    def tearDown(self):
        if os.path.exists(self.bank_file):
            os.remove(self.bank_file)
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)
             
    def test_getting_emme2_data_into_travel_data_set(self):
        tm_output = TravelModelOutput()
        tm_output._put_one_matrix_into_travel_data_set(self.travel_data_set, 
                                                               3,
                                                               'au1tim', 
                                                               'single_vehicle_to_work_travel_time',
                                                               'Bank1', 
                                                               self.bank_storage)
        self.assertEqual(self.travel_data_set.get_attribute('single_vehicle_to_work_travel_time').size, 9)
        self.assertEqual(allclose(self.travel_data_set.get_attribute('single_vehicle_to_work_travel_time'), 
                                  array([2,5,7,3, 7.9, 1.3, 6,10,0])), True)

    def test_getting_several_emme2_data_into_travel_data_set(self):
        matrix_attribute_map = {'au1tim':'single_vehicle_to_work_travel_time',
                                'biketm':'bike_to_work_travel_time'}
        tm_output = TravelModelOutput()
        travel_data_set = tm_output.get_travel_data_set(self.zone_set, matrix_attribute_map, 
                                                        in_storage=self.bank_storage, table_name='Bank1')
        self.assertEqual(travel_data_set.get_attribute('single_vehicle_to_work_travel_time').size, 9)
        self.assertEqual(travel_data_set.get_attribute('bike_to_work_travel_time').size, 9)
        self.assertEqual(False,
                             allclose(travel_data_set.get_attribute('single_vehicle_to_work_travel_time'), 
                                      travel_data_set.get_attribute('bike_to_work_travel_time')))
        self.assertEqual(allclose(travel_data_set.get_attribute('single_vehicle_to_work_travel_time'), 
                                  array([2,5,7,1.3, 7.9, 3, 6,10,0])), True)
        self.assertEqual(allclose(travel_data_set.get_attribute('bike_to_work_travel_time'), 
                                  array([10,50,65, 13, 10.9, 40, 56,100,21])), True)
        
if __name__=='__main__':
    opus_unittest.main()