# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
import os
import shutil
from numpy import sort, zeros, sqrt
from opus_core.bayesian_melding import BayesianMelding
from opus_core.bayesian_melding import ObservedData
from opus_core.plot_functions import plot_histogram
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool


if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # What directory contains the multiple runs'
    #cache_directory = "/Users/hana/workspace/data/psrc_parcel/runs"
    cache_directory = "/Volumes/D Drive TMOD3/opus/data/psrc_parcel/runs"
    # Where the observed data is stored
    observed_data_dir = "/Users/hana/workspace/data/psrc_parcel/observed_data"

    observed_data = ObservedData(observed_data_dir, 
                                 year=2008, # from what year are the observed data 
                                 storage_type='tab_storage', # in what format
                                 package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])

    known_output=[
                  {'variable_name': "urbansim_parcel.zone.number_of_households", # What variable does the observed data correspond to
                   'filename': "households2008", # In what file are values of this variable
                   'transformation': "sqrt", # What transformation should be performed (can be set to None)
                   # Other arguments of the class ObservedDataOneQuantity (in bayesian_melding.py) can be set here. See its doc string.
                   #'filter': "urbansim_parcel.zone.number_of_households", 
                   },
#                    {'variable_name': "travel_data.am_single_vehicle_to_work_travel_time",
#                     'filename': "travel_times", 
#                     'transformation': "sqrt",
#                   #'filter': "urbansim_parcel.zone.number_of_households",
#                   },
                  {'variable_name': "urbansim_parcel.zone.number_of_jobs",
                   'filename': "jobs2008", 
                   'transformation': "sqrt",
                   #'filter': "urbansim_parcel.zone.number_of_jobs",
                   },
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
        
#    for group in ['mining', 'constr', 'retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
#        known_output = known_output + [
#                {'variable_name': "urbansim_parcel.zone.number_of_jobs_of_sector_group_%s" % group,
#                   'filename': "jobs_by_zones_and_groups", 
#                   'transformation': "sqrt",
#                   }]
          
    for quantity in known_output:
        observed_data.add_quantity(**quantity)
        
    bm = BayesianMelding(cache_directory, 
                         observed_data,                        
                         base_year=2000, 
                         prefix='run_31', # within 'cache_directory' filter only directories with this prefix
                         package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    
    weights = bm.compute_weights()
    print weights
    
    variable_list = map(lambda x: x.get_alias(), bm.observed_data.get_variable_names())
    n = len(variable_list)
    for index in range(n):
        name = variable_list[index]
        print name
        print "variance: ", bm.get_variance()[index]
        print "variance mean: ", bm.get_variance()[index].mean(), " sd: ", sqrt(bm.get_variance()[index].var())
        print "bias:", bm.get_bias()[index] 
        print "weight components: ", bm.get_weight_components()[index]
    
    from numpy import argsort
    w = bm.get_weights()
    maxiall = argsort(w)[-1]
    print "all weights: max = %s, index = %s" % (w[maxiall], maxiall)
#    maxi3all = argsort(w)[range(-1,-4,-1)]
#    miniall =  argsort(w)[0]
#    for index in range(n):
#        name = variable_list[index]
#        wc = bm.get_weight_components()[index]
#        maxi = argsort(wc)[-1]
#        print "%s: max = %s, index = %s, w[%s] = %s" % (name, wc[maxi], maxi, maxiall, wc[maxiall])
#        print wc[maxi3all], wc[miniall]

    bm.export_bm_parameters('/Users/hana/workspace/data/psrc_parcel/runs/bmanal', filename='bm_parameters')
    #bmf = BayesianMeldingFromFile("/Users/hana/bm/psrc_parcel/simulation_results/0818/2005/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'])
    
    ####
    # The code below has not been tested for a while and might not work 
    ####
    #bm.plot_boxplot_r('bm_plot.pdf', weight_threshold=0.1)
    bm.export_weights_posterior_mean_and_variance([2008, 2010, 2030, 2040], quantity_of_interest="urbansim_parcel.zone.number_of_households",
              directory="/Users/hana/workspace/data/psrc_parcel/runs/bmanal")
#    bm.export_weights_posterior_mean_and_variance([2020], quantity_of_interest="urbansim_parcel.zone.number_of_jobs",
#                            directory="/Users/hana/bm/psrc_parcel/simulation_results")
    
#    posterior = bm.generate_posterior_distribution(year=2040, quantity_of_interest="urbansim_parcel.zone.number_of_households",
#                                                   replicates=1000)

    #posterior = bm.generate_posterior_distribution(year=2010, quantity_of_interest="urbansim_parcel.zone.number_of_households",
    #                                               replicates=1000)

    #bm.write_simulated_values("/Users/hana/workspace/data/psrc_parcel/runs/bmanal/simulated_values")
    #bm.write_values_from_multiple_runs("/Users/hana/multiple_run_values")

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
    
def convert_screenline_report_to_dataset(report_name, cache_directory, years):
    """This is an obsolete function (not used)."""
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