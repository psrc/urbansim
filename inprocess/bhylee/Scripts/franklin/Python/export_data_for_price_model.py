
#   From Liming:
#Hi Joel,
#You can use the following steps to export building variables to a csv file.
#First, specify in repm_specification.py all varaibles you'll possibly use;
#Second, start estimation with command: python -i run_estimation.py;
#Third, in the python prompt after estimation, enter the following commands:

buildings=er.estimator.model_system.run_year_namespace['building']
from opus_core.store.delimited_storage import delimited_storage
#replace storage_location with location in directory in your hdd
outstorage = delimited_storage(storage_location='c:/urbansim_cache/',
                               delimiter = ',', file_extension='csv')
buildings.write_dataset(out_storage=outstorage,
                    out_table_name='buildings',
                    attributes=buildings.get_known_attribute_names())
#or replace the last line with: attributes=['building_id', 'gc_da_to_cbd','parcel_sqft']
#to only export variables you want
