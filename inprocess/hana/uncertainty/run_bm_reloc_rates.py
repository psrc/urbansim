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
from opus_core.datasets.dataset import Dataset


if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # What directory contains the multiple runs'
    cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/relocation/0122"

    # Where the observed data is stored
    observed_data_dir = "/Users/hana/urbansim/census"

    observed_data = ObservedData(observed_data_dir, 
                                 year=2001, # from what year are the observed data 
                                 storage_type='tab_storage', # in what format
                                 package_order=['inprocess', 'psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])

    known_output=[
                  {'variable_name': 'inprocess.household_relocation_rate.annual_relocation_rate', # What variable does the observed data correspond to
                   'filename': "household_relocation_rates", # In what file are values of this variable
                   'transformation': 'sqrt', # What transformation should be performed (can be set to None)
                   # Other arguments of the class ObservedDataOneQuantity (in bayesian_melding.py) can be set here. See its doc string.
                   #'filter': "urbansim_parcel.zone.number_of_households", 
                   "id_name":[]
                   },
                  ]
          
    for quantity in known_output:
        observed_data.add_quantity(**quantity)
        
    rate_storage = StorageFactory().get_storage('tab_storage',  storage_location = observed_data_dir)
    rates = Dataset(in_storage = rate_storage, 
                in_table_name='household_relocation_rates', id_name=[], dataset_name='household_relocation_rate')
    rates.delete_one_attribute('annual_relocation_rate')
    bm = BayesianMelding(cache_directory, 
                         observed_data,                        
                         base_year=2000, 
                         prefix='run_', # within 'cache_directory' filter only directories with this prefix
                         package_order=['inprocess', 'psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                         additional_datasets = {'household_relocation_rate': rates})
    
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
    maxi3all = argsort(w)[range(-1,-4,-1)]
    miniall =  argsort(w)[0]
    for index in range(n):
        name = variable_list[index]
        wc = bm.get_weight_components()[index]
        maxi = argsort(wc)[-1]
        print "%s: max = %s, index = %s, w[%s] = %s" % (name, wc[maxi], maxi, maxiall, wc[maxiall])
        print wc[maxi3all], wc[miniall]
        
    bm.write_expected_values('/Users/hana/urbansim_cache/psrc/parcel/bm/relocation/0122/bm_output/mu', 0)
    
    #bm.export_bm_parameters('/Users/hana/bm/psrc_parcel/simulation_results/0818/2005', filename='bm_parameters')
    #bmf = BayesianMeldingFromFile("/Users/hana/bm/psrc_parcel/simulation_results/0818/2005/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'])
    
    ####
    # The code below has not been tested for a while and might not work 
    ####
    #bm.plot_boxplot_r('bm_plot.pdf', weight_threshold=0.1)
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
