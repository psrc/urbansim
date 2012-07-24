# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from pandas import read_csv, DataFrame
import os, glob, re
from itertools import product
import numpy as np
from numpy import array
from opus_core.logger import logger, log_block
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory

def read_csv_with_numpy(in_fname, columns=[], header=True):
    skiprows = 0
    if header:
        f = file(in_fname)
        skiprows = 1
        header = f.readline().strip().split(",")
        columns = [v.lower() for v in header]
        f.close()
    #names = ['from_zone_id', 'to_zone_id', 'travel_time']
    formats = ['i4', 'i4', 'f4']
    dtype = {'names': columns, 'formats':formats}
    data = np.loadtxt(in_fname, dtype=dtype,
                      skiprows=skiprows, delimiter=",")
    return data

def avg_travel_time(skims, hours, prefix='tm'):
    count = 1
    attr_pattern = '{}{}'
    avg_tt = skims[attr_pattern.format(prefix, str(0))] * 0.0
    for hour in hours:
        avg_tt += skims[attr_pattern.format(prefix, str(hour))]
        count += 1

    avg_tt /= count
    return avg_tt

def to_opus_dataset(df, out_store, table_name):
    data_dict = {}
    id_names = df.index.names
    df = df.reset_index()
    for name in df.columns:
        data_dict[name] = df[name].values
    in_store = StorageFactory().get_storage('dict_storage')
    in_store.write_table(table_name=table_name,
                        table_data=data_dict) 
    opus_ds = Dataset(in_storage=in_store,
                    in_table_name=table_name,
                    id_name=id_names,
                    dataset_name='dataset')
    opus_ds.write_dataset(attributes='*', out_storage=out_store,
                          out_table_name=table_name)
    return opus_ds

@log_block()
def import_openamos_data(config, year, zone_set):
    tm_config = config['travel_model_configuration']
    openamos_dir = tm_config[year]
    #skim_dir = "/workspace/workdata/SimTRAVEL_data/base_scenario/skims/bootstrap/"
    skim_dir = os.path.join(openamos_dir, "skims/bootstrap")
    logger.log_status('Reading skims from {}'.format(skim_dir))
    skim_files = glob.glob(os.path.join(skim_dir, "skim*.dat"))
    skims = None
    """
    for skim_file in skim_files:
        i = int( re.search('\d+', skim_file).group(0) )
        skim = read_csv_with_numpy(skim_file, header=False,
                                   columns=['from_zone_id', 'to_zone_id', str(i)])
        if skims is None:
            skims = skim
        else:
            import pdb; pdb.set_trace()
            skims = np.hstack((skims, skim[str(i)]))
    """
    attr_pattern = '{}{}'
    for skim_file in skim_files:
        i = int( re.search('\d+', skim_file).group(0) )
        skim = read_csv(skim_file, header=0,
                        names=['from_zone_id', 'to_zone_id', 'travel_time', 'travel_distance'])
        if skims is None:
            skims = skim.rename(columns={'travel_time': attr_pattern.format('tm', str(i)),
                                         'travel_distance': attr_pattern.format('td', str(i)),
                                        }, copy=False)
        else:
            #skims.insert(i, str(i), skim.travel_time
            skims[attr_pattern.format('tm', str(i))] = skim.travel_time
            skims[attr_pattern.format('td', str(i))] = skim.travel_distance

    skims.set_index(['from_zone_id', 'to_zone_id'], inplace=True)

    peak_hours = set([6, 7, 8, 9, 16, 17, 18, 19])
    off_peak_hours = set(range(24)) - peak_hours
    peak_travel_time = avg_travel_time(skims, peak_hours, prefix='tm')
    off_peak_travel_time = avg_travel_time(skims, off_peak_hours, prefix='tm')
    peak_travel_distance = avg_travel_time(skims, peak_hours, prefix='td')
    off_peak_travel_distance = avg_travel_time(skims, off_peak_hours, prefix='td')
    travel_time = DataFrame({'peak_travel_time': peak_travel_time, 
                             'off_peak_travel_time': off_peak_travel_time,
                             'peak_travel_distance': peak_travel_distance, 
                             'off_peak_travel_distance': off_peak_travel_distance,
                            })

    ## subset to include only zones appearing in zone_set
    #zone_ids = zone_set['zone_id']
    #zone_pairs = [z for z in product(zone_ids, zone_ids)]
    #travel_time = travel_time.ix[zone_pairs]

    cache_directory = config['cache_directory']
    simulation_state = SimulationState()
    simulation_state.set_current_time(year)
    simulation_state.set_cache_directory(cache_directory)
    out_store = AttributeCache().get_flt_storage_for_year(year+1)
    logger.log_status('Caching travel_data to {}'.format(out_store.get_storage_location()))
    travel_data = to_opus_dataset(travel_time, out_store, 'travel_data')

    return travel_data
    #travel_time.to_csv('/some/where/travel_data.csv')

from opus_core.tests import opus_unittest
import tempfile, shutil

class Tests(opus_unittest.OpusTestCase):
    """unittest"""
    def test_import_openamos_data(self):
        #openamos_dir = '/workspace/opus/data/mag_zone/simtravel_data/base_scenario/'
        openamos_dir = '/workspace/opus/data/mag_zone/simtravel_data/skims_with_travel_dist/'
        if not os.path.exists(openamos_dir):
            logger.log_status('openamos skims not found in {}; unittest skipped'.format(openamos_dir))
            return
        tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')
        print tmp_dir
        config = {'travel_model_configuration': {2000: openamos_dir},
                  'cache_directory': tempfile.mkdtemp(prefix='urbansim_tmp')}
        zone_set = {'zone_id': array([1,3,6])}
        results = import_openamos_data(config, 2000, zone_set)
        assert os.path.exists(config['cache_directory']+'/2001/travel_data')
        assert results.size() == 9
        attr_names = results.get_known_attribute_names()
        attr_names.sort()
        assert np.all(attr_names == ['from_zone_id', 'off_peak_travel_time',
                                        'peak_travel_time', 'to_zone_id'])
        #shutil.rmtree(tmp_dir)

if __name__ == '__main__':
    opus_unittest.main()
