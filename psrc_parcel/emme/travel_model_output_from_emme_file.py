# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import zeros, float32, indices, array, arange, where, repeat, tile
from opus_core.storage_factory import StorageFactory
import os
from operator import itemgetter

from opus_emme2.travel_model_output import TravelModelOutput as ParentTravelModelOutput

class TravelModelOutput(ParentTravelModelOutput):
    """
    A class to access the output of emme4 travel models from an ascii file.
    """

    def get_travel_data_set(self, zone_set, matrix_attribute_name_map, 
                            out_storage=None, **kwargs):
        """
        Returns a new travel data set containing the given set of emme matrices 
        populated from an ascii file. The columns in the travel data set are 
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
        path = in_storage.load_table(table_name)['path']
        use_postfix = None
        for postfix in ['rpf', 'rp4', 'rp3', 'rp2', 'rp1', 'rp0']:
            if os.path.exists(os.path.join(path, "mf%s.%s" % (matrix_name, postfix))):
                use_postfix = postfix
                break
        if use_postfix is None:
            raise IOError, "Skim %s not available in %s" % (matrix_name, path)
        try:
            file_contents = self._get_emme2_data_from_file(os.path.join(path, "mf%s.%s" % (matrix_name, use_postfix)))                      
            travel_data_set.add_primary_attribute(data=zeros(travel_data_set.size(), dtype=float32), 
                                                  name=attribute_name)
            file_contents = [line.replace(':', ' ') for line in file_contents]
            file_contents = [line.replace('*****', '999') for line in file_contents]
            attr = zeros((max_zone_id, max_zone_id), dtype=float32)
            
            ind = arange(1,14,2)
            valind = arange(2,15,2)
            #getter_values = itemgetter(range(3,l,2))
            #getter_index = itemgetter(range(2,l-1,2))
            for line in file_contents:
                v = array(line.split())
                if int(v[0]) > max_zone_id:
                    continue
                l = v.size
                to_zones = v[ind[:(l-1)/2]].astype('int32')
                valid = where(to_zones <= max_zone_id)[0]
                attr[v[0].astype('int32')-1, to_zones[valid]-1] = (v[valind[:(l-1)/2]][valid]).astype(float32)
            if attr.size == 0:
                logger.log_error("Skipped exporting travel_data attribute %s: No data is exported from EMME matrix." % attribute_name)
            else:
                zones = arange(1,max_zone_id+1)
                Ozones = repeat(zones, max_zone_id)
                Dzones = tile(zones, (max_zone_id, 1)).flatten()
                travel_data_set.set_values_of_one_attribute_with_od_pairs(attribute=attribute_name,
                                                                          values=attr.flatten(),
                                                                          O=Ozones, D=Dzones)
        finally:
            logger.end_block()
            
