#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os
from numpy import zeros, round_, clip
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset


class ScenarioDifferences:
    def run(self, cache1, cache2, indicators, dataset_name, id_name, percentage=False, write_dataset=False, round_to_integer=False):
        tab_storage1 = StorageFactory().get_storage('tab_storage',storage_location = os.path.join(cache1,'indicators'))
        tab_storage2 = StorageFactory().get_storage('tab_storage',storage_location = os.path.join(cache2,'indicators'))
        
        dataset = None
        for indicator in indicators:
            if dataset is None:
                dataset = Dataset(in_storage=tab_storage1, dataset_name=dataset_name, in_table_name=indicator, id_name=id_name)
            else:
                tmp_dataset = Dataset(in_storage=tab_storage1, in_table_name=indicator, id_name=id_name)
                for attr in tmp_dataset.get_known_attribute_names():
                    if attr <> id_name:
                        dataset.add_attribute(data=tmp_dataset.get_attribute(attr), name=attr, metadata=1)
                        if percentage:
                            dataset.add_attribute(data=zeros(tmp_dataset.size()), name='p_%s' % attr, metadata=1)
                    
            tmp_dataset = Dataset(in_storage=tab_storage2, in_table_name=indicator, id_name=id_name)
            for attr in tmp_dataset.get_known_attribute_names():
                d = dataset.get_attribute(attr)-tmp_dataset.get_attribute(attr)
                if round_to_integer:
                    d = round_(d).astype('int32')
                dataset.modify_attribute(name=attr, data=d)
                if percentage:
                    dataset.add_primary_attribute(name='p_%s' % attr, 
                                                  data=round_(d/(clip(tmp_dataset.get_attribute(attr), 1,tmp_dataset.get_attribute(attr))/100.0),0).astype('int32'))
        if write_dataset:
            storage = StorageFactory().get_storage('flt_storage',storage_location = cache1)
            dataset.write_dataset(out_storage=storage, out_table_name=dataset_name)
        return dataset
    
if __name__ == "__main__":
    
    cache1 = '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_6434_full_pe'
    cache2 = '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_6433_full_pe'
    #indicators = ['zone__tab__nohhs', 'zone__tab__nojs']
    #indicators = ['faz__tab__hhs', 'faz__tab__jobs']
    #indicators = ['faz__tab__vmtf', 'faz__tab__vtf']
    indicators = ['faz__tab__amvmtph']
    #indicators = []
    #for group in ['retail', 'manu', 'wtcu', 'fires', 'gov', 'edu', 'mining', 'constr']:
    #    indicators.append('faz__tab__%s' % group)
    #indicators = ['zone__tab__tt_to_136', 'zone__tab__tt_to_285']
    new_table_name = None # table given by table_name will be overwritten
    #new_table_name = 'zones_nv_minus_v'
    #new_table_name = 'faz_nv_minus_v'
    dataset = ScenarioDifferences().run(cache1, cache2, indicators, new_table_name, 'faz_id', percentage=False, round_to_integer=False)
    
    #dbf_dir = '/Users/hana/GIS_data/Zones'
    dbf_dir = '/Users/hana/GIS_data/Geographies'
    #table_name = 'taz2000_polygon'
    #table_name = 'zones_nv_minus_v'
    #join_attribute = 'taz'
    #table_name = 'faz'
    table_name = 'faz_nv_minus_v'
    join_attribute = 'faz'
    attribute_names = dataset.get_known_attribute_names()
    #attribute_names = ['am_single_vehicle_to_work_travel_time', 'md_vehicle_miles_traveled', 'single_vehicle_to_work_travel_cost']
    from opus_core.tools.spatial_table_join import SpatialTableJoin
    SpatialTableJoin().run(table_name, 'dbf_storage', data_path=dbf_dir, dataset=dataset, attribute_names=attribute_names, 
                         join_attribute=join_attribute, new_table_name=new_table_name)
        
    