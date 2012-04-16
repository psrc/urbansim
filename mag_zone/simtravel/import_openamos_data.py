
from pandas import read_csv
import os, glob, re

def avg_travel_time(skims, hours):
    count = 1
    avg_tt = skims[0] * 0.0
    for hour in hours:
        avg_tt += skims[hour]
        count += 1

    avg_tt /= count
    return avg_tt

def to_opus_dataset(df, cache_dir, table_name):
    data_dict = {}
    id_names = df.index.names
    df.reset_index()
    for name in df.columns:
        data_dict[name] = df[name].values

    in_store = StorageFactory().get_storage('dict_storage')
    out_storage = StorageFactory().get_storage(
       type='flt_storage',
       subdir='store',
       storage_location=config['storage_location'])    
    out_store = StorageFactory().get_storage('flt_storage')(cache_dir)
    in_store.write_table(table_name=table_name,
                        table_data=data_dict) 
    opus_ds = Dataset(in_storage=in_store,
                    in_table_name=table_name,
                    id_name=id_names,
                    dataset_name='dataset')
    opus_ds.write_dataset(attributes='*', out_storage=out_store)

#@log
def import_openamos_data(config, year, zone_set):
    tm_config = config['travel_model_configuration']
    openamos_dir = tm_config[year]
    #path = "/workspace/workdata/SimTRAVEL_data/base_scenario/skims/bootstrap/"
    skim_files = glob.glob(os.path.join(openamos_dir, "skims/bootstrap/skim*.dat"))
    skims = {}
    for skim_file in skim_files:
        i = int( re.search('\d+', skim_file).group(0) )
        skims[i] = read_csv(skim_file, header=0,
                           names=['from_zone_id', 'to_zone_id', 'travel_time'])
        skims[i].set_index(['from_zone_id', 'to_zone_id'], inplace=True)

    peak_hours = set([6, 7, 8, 4, 5, 6])
    off_peak_hours = set(range(24)) - peak_hours

    peak_travel_time = avg_travel_time(skims, peak_hours)
    off_peak_travel_time = avg_travel_time(skims, off_peak_hours)
    travel_time = peak_travel_time + off_peak_travel_time
    ## subset to include only zones appearing in zone_set
    zone_ids = zone_set.get_id_attribute()
    travel_time = travel_time.take(zip(zone_ids, zone_ids))

    to_opus_dataset(travel_time, cache_dir, 'travel_data')
    #travel_time.to_csv('/some/where/travel_data.csv')
