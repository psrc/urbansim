import sys
import os
import shutil
from numpy import sort, zeros, sqrt, newaxis, concatenate, array, round_
from opus_core.bayesian_melding import BayesianMelding
from opus_core.bayesian_melding import ObservedData
from opus_core.plot_functions import plot_histogram
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.misc import write_table_to_text_file, write_to_text_file

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # What directory contains the multiple runs'
    cache_directory = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs"
    #cache_directory = "/Users/hana/d$/opusgit/urbansim_data/data/psrc_parcel/runs"
    #cache_directory = "d:/opusgit/urbansim_data/data/psrc_parcel/runs"
    cache_dir_file = "cache_directories_local.txt"
    #cache_dir_file = "cache_directories.txt"

    result_directory = "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/bm33_32"
    #result_directory = "d:/opusgit/urbansim_data/data/psrc_parcel/runs/bm_36_37"
    # Where the observed data is stored
    observed_data_dir = "/Users/hana/opus/urbansim_data/data/psrc_parcel/observed_data"
    observed_data_dir = "/Users/hana/psrc/R/uncertainty/data"
    #observed_data_dir = "d:/opusgit/urbansim_data/data/psrc_parcel/observed_data"

    variables = {"households": {"zone": "urbansim_parcel.zone.number_of_households",
                                "faz": "number_of_households = faz.aggregate(urbansim_parcel.zone.number_of_households)",
                                "city": "number_of_households = city.aggregate(urbansim_parcel.parcel.number_of_households)",
                                "fips_rgs": "number_of_households = fips_rgs.aggregate(urbansim_parcel.parcel.number_of_households, intermediates=[city])"},
                 "employment": {"zone": "urbansim_parcel.zone.number_of_jobs",
                                "faz": "number_of_jobs = faz.aggregate(urbansim_parcel.zone.number_of_jobs)",
                                "city": "number_of_jobs = city.aggregate(urbansim_parcel.parcel.number_of_jobs)",
                                "fips_rgs": "number_of_jobs = fips_rgs.aggregate(urbansim_parcel.parcel.number_of_jobs, intermediates=[city])"}
                 }

    geos = ["zone", "faz", "city", "fips_rgs"]
    geos = ["fips_rgs"]
    observed_data = {}
    known_output = {}
    bmgeos = {}
    for geo in geos:
        observed_data[geo] = ObservedData(observed_data_dir, 
                                 year=2017, # from what year are the observed data 
                                 storage_type='csv_storage', # in what format
                                 package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
  
        known_output[geo] = [
            {
                'variable_name': variables["households"][geo], # What variable does the observed data correspond to
                'filename': "ofm_hh17_%s" % geo, # In what file are values of this variable
                'transformation': "sqrt", # What transformation should be performed (can be set to None)
                # Other arguments of the class ObservedDataOneQuantity (in bayesian_melding.py) can be set here. See its doc string.
                #'filter': "urbansim_parcel.zone.number_of_households", 
            },
            {
                'variable_name': variables["employment"][geo],
                'filename': "jobs2016_%s" % geo, 
                'transformation': "sqrt",
                #'filter': "urbansim_parcel.zone.number_of_jobs",
            }]
    
        for quantity in known_output[geo]:
            observed_data[geo].add_quantity(**quantity)    
        
        bmgeos[geo] = BayesianMelding(
                         os.path.join(result_directory, cache_dir_file),
                         observed_data[geo],                        
                         base_year=2014, 
                         #prefix='run_32.', # within 'cache_directory' filter only directories with this prefix
                         #overwrite_cache_directories_file=True,
                         package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                         output_dir = "bm_output_%s" % geo) 
    
    if not os.path.exists(result_directory):
        os.mkdir(result_directory)
        
    indicators = {"households": "number_of_households", "employment": "number_of_jobs"}
    for geo, bm in bmgeos.iteritems():
        print geo
        print "======="
        # Main computation
        weights = bm.compute_weights()
        print weights 
        # compute and export CIs
        for year in [2017, 2040, 2050]:
            for indkey, indvalue in indicators.iteritems():
                bm.set_posterior(year, quantity_of_interest=variables[indkey][geo],
                                 propagation_factor=[0,1])
                med = bm.get_exact_quantile(0.5)
                ci80 = bm.get_probability_interval(80)
                ci95 = bm.get_probability_interval(95)
                filename = os.path.join(result_directory, "%s_%s_%s.txt" % (year, geo, indkey))
                write_to_text_file(filename, array(["id", "median", "lower_80", "upper_80", "lower_95", "upper_95"]), delimiter="\t")
                write_table_to_text_file(filename, round_(concatenate((bm.get_m_ids()[:,newaxis], med[:,newaxis], ci80, ci95), axis=1)), mode = "a", delimiter="\t")
    
    
        
    #bm.export_confidence_intervals([80, 95], "/Users/hana/opus/urbansim_data/data/psrc_parcel/runs/testCI")
    #bm.export_weights_posterior_mean_and_variance([2017, 2040], quantity_of_interest="urbansim_parcel.zone.number_of_households", 
    #                                              directory=cache_directory, propagation_factor=[0,1])
    add_to_file=False
    for i in [0,1]:
        bm.export_bm_parameters(cache_directory, filename='bm_parameters', add_to_file=add_to_file, run_index=i)
        add_to_file=True
    print 
#    variable_list = map(lambda x: x.get_alias(), bm.observed_data.get_variable_names())
#    n = len(variable_list)
#    for index in range(n):
#        name = variable_list[index]
#        print name
#        print "variance: ", bm.get_variance()[index]
#        print "variance mean: ", bm.get_variance()[index].mean(), " sd: ", sqrt(bm.get_variance()[index].var())
#        print "bias:", bm.get_bias()[index] 
#        print "weight components: ", bm.get_weight_components()[index]
    
#    from numpy import argsort
#    w = bm.get_weights()
#    maxiall = argsort(w)[-1]
#    print "all weights: max = %s, index = %s" % (w[maxiall], maxiall)

#    maxi3all = argsort(w)[range(-1,-4,-1)]
#    miniall =  argsort(w)[0]
#    for index in range(n):
#        name = variable_list[index]
#        wc = bm.get_weight_components()[index]
#        maxi = argsort(wc)[-1]
#        print "%s: max = %s, index = %s, w[%s] = %s" % (name, wc[maxi], maxi, maxiall, wc[maxiall])
#        print wc[maxi3all], wc[miniall]

    # Export results for later use
    #bm.export_bm_parameters('/Users/hana/workspace/data/psrc_parcel/runs/bmanal', filename='bm_parameters')
    # Reload results 
    #bmf = BayesianMeldingFromFile("/Users/hana/bm/psrc_parcel/simulation_results/0818/2005/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'])
    
    # Export means and variance into an ASCII table
    #bm.export_weights_posterior_mean_and_variance([2008, 2010, 2030, 2040], quantity_of_interest="urbansim_parcel.zone.number_of_households",
    #          directory="/Users/hana/workspace/data/psrc_parcel/runs/bmanal")
#    bm.export_weights_posterior_mean_and_variance([2020], quantity_of_interest="urbansim_parcel.zone.number_of_jobs",
#                            directory="/Users/hana/bm/psrc_parcel/simulation_results")
    
    # To export confidence intervals:
    # -- zone geography
    posterior = bm.generate_posterior_distribution(year=2040, quantity_of_interest="urbansim_parcel.zone.number_of_households",
                                                   replicates=1000, propagation_factor=[0,1])
    ci = bm.export_confidence_intervals([80, 95], "/Users/hana/workspace/data/psrc_parcel/runs/bmanal/2040_conf_intervals_zones.txt")
    # -- large area geography
    posterior = bm.generate_posterior_distribution(year=2040, quantity_of_interest="urbansim_parcel.zone.number_of_households",
                                                   aggregate_to="large_area", intermediates=['faz'], replicates=1000, propagation_factor=[0,1])
    ci = bm.export_confidence_intervals([80, 95], "/Users/hana/workspace/data/psrc_parcel/runs/bmanal/2040_conf_intervals_large_areas.txt")


###########
    # Other functions
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
