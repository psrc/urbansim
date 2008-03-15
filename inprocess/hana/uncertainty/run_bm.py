#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

import sys
import os
import shutil
from numpy import sort, zeros
from opus_core.bayesian_melding import BayesianMelding
from opus_core.bayesian_melding import ObservedData
from opus_core.plot_functions import plot_histogram
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.faz_dataset import FazDataset
from urbansim.datasets.large_area_dataset import LargeAreaDataset
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_pool import DatasetPool

def convert_screenline_report_to_dataset(report_name, cache_directory, years):
    for year in years:
        dir = os.path.join(cache_directory, str(year))
        flt_storage = StorageFactory().get_storage('flt_storage',storage_location = dir)
        pool = DatasetPool(storage=flt_storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
        scnodes = pool.get_dataset('screenline_node')
        scnodes.add_primary_attribute(name='traffic_volume_eh', data=zeros(scnodes.size(), dtype='float32'))
        full_report_name = os.path.join(dir, report_name)
        file = open(full_report_name, 'r')
        file_contents = map(str.strip, file.readlines())
        not_found_counter = 0
        for line in file_contents[1:len(file_contents)]:
            node_i, node_j, value, dummy = str.split(line)
            try:
                scnodes.set_value_of_attribute_by_id(attribute='traffic_volume_eh', value=float(value), 
                                                             id=(int(node_i), int(node_j)))
            except:
                not_found_counter+=1
        print "%s nodes not found in year %s" % (not_found_counter, year)
        scnodes.write_dataset(out_storage=flt_storage)    

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # set true_data_cache if the true data are stored in a cache (in the same way as an urbansim cache)
    #true_data_cache = "/scratch/urbbuild/urbansim_cache/psrc/uncertainty/run_1364.2006_12_01_10_42"

    # in what directory is the file 'cache_directories'
    #cache_directory = "/home/hana/urbansim_cache/psrc/parcel/run_3904.2007_10_19_15_01"
    #cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/1211/run_4491.2007_12_11_13_58"
    #cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/0123/run_4960.2008_01_23_10_09"
    #cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/0124/run_4954.2008_01_23_09_59"
    #cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/0131/run_5090.2008_01_31_14_45"
    cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/0307/run_5737_point_est"
    # where the true data (on a zone level) is stored in a table format 
    observed_data_dir = "/Users/hana/bm/observed_data/"

    observed_data = ObservedData(observed_data_dir, 2005, 'tab_storage', 
                                 package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])

    known_output=[
                  {'variable_name': "urbansim_parcel.zone.number_of_households",
                   'filename': "PSRC2005TAZDataNew", 
                   'transformation': "sqrt",
                   #'filter': "urbansim_parcel.zone.number_of_households",
                   },
#                    {'variable_name': "travel_data.am_single_vehicle_to_work_travel_time",
#                     'filename': "travel_times", 
#                     'transformation': "sqrt",
#                   #'filter': "urbansim_parcel.zone.number_of_households",
#                   },
#                  {'variable_name': "urbansim_parcel.zone.number_of_jobs",
#                   'filename': "PSRC2005TAZDataNew", 
#                   'transformation': "sqrt",
#                   #'filter': "urbansim_parcel.zone.number_of_jobs",
#                   },
#                   {'variable_name': "urbansim_parcel.zone_x_employment_sector.number_of_jobs",
#                   'filename': "jobs_by_zones_and_sectors_flatten", 
#                   'transformation': "sqrt",
#                   "id_name":  ["zone_id", "sector_id"]
#                   },
#                   {'variable_name': "psrc_parcel.screenline.traffic_volume_eh",
#                    'filename': "screenlines",
#                    'filter': "psrc_parcel.screenline.traffic_volume_eh",
#                    'transformation': "sqrt",
#                    'dependent_datasets': {'screenline_node': {'filename':'tv2006', 'match': True}}
#                    }
#                  {'variable_name': "urbansim_parcel.faz_x_land_use_type.total_value_per_sqft",
#                   'filename': "avg_total_value_per_unit_by_faz", 
#                   'transformation': "log",
#                   'filter': 'faz_x_land_use_type_flatten.total_value_per_sqft > 0',
#                   "id_name":  ["faz_id", "land_use_type_id"]
#                   },
#                  {'variable_name': "urbansim_parcel.large_area_x_land_use_type.total_value_per_sqft",
#                   'filename': "avg_total_value_per_unit_by_la", 
#                   'transformation': "log",
                   #'filter': 'faz_x_land_use_type_flatten.total_value_per_sqft > 0',
#                   "id_name":  ["large_area_id", "land_use_type_id"]
#                   }
                  ]
                  
#    for sector in range(1,20):
#        known_output = known_output + [
#                {'variable_name': "urbansim_parcel.zone.number_of_jobs_of_sector_%s" % sector,
#                   'filename': "jobs_by_zones_and_sectors", 
#                   'transformation': "sqrt",
#                   }]
        
    for group in ['mining', 'constr', 'retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
        known_output = known_output + [
                {'variable_name': "urbansim_parcel.zone.number_of_jobs_of_sector_group_%s" % group,
                   'filename': "jobs_by_zones_and_groups", 
                   'transformation': "sqrt",
                   }]
          
    for quantity in known_output:
        observed_data.add_quantity(**quantity)
        
    #convert_screenline_report_to_dataset('tveham.rpt', cache_directory, [2006, 2011])
                                         #[2006,2011, 2016, 2021])
    bm = BayesianMelding(cache_directory, 
                         observed_data,                        
                         base_year=2000, 
                         #scaling_parents = scaling,
                         package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    weights = bm.compute_weights()
    print weights
#    bm.export_weights_posterior_mean_and_variance([2020], quantity_of_interest="urbansim_parcel.zone.number_of_households",
#              directory="/Users/hana/bm/psrc_parcel/simulation_results")
#    bm.export_weights_posterior_mean_and_variance([2020], quantity_of_interest="urbansim_parcel.zone.number_of_jobs",
#                            directory="/Users/hana/bm/psrc_parcel/simulation_results")
    
    #posterior = bm.generate_posterior_distribution(year=2015, quantity_of_interest="urbansim_parcel.zone.number_of_households",
                                                  # replicates=1000)

    #bm.write_simulated_values("/Users/hana/simulated_values")
    #bm.write_values_from_multiple_runs("/Users/hana/multiple_run_values")
    #bm.write_simulated_values("/home/hana/BM/psrc_analysis/data/simulated_values")
    #bm.write_values_from_multiple_runs("/home/hana/BM/psrc_analysis/data/multiple_run_values")

    #bm.compute_y()
    #bm.compute_and_write_true_data(2002, "urbansim.zone.population", "/Users/hana/observations")
    #bm.compute_and_write_true_data(2006, "urbansim.zone.population", "/home/hana/BM/psrc_analysis/data/observations")

    #for k in range(posterior.shape[0]):
     #   plot_histogram(posterior[k,:], bins=50)
     
    #m = bm.get_quantity_from_simulated_values("mean")
    #print m
    #std = bm.get_quantity_from_simulated_values("standard_deviation")
    #print std
    #prob = bm.get_probability_interval(0.8)
    #print prob