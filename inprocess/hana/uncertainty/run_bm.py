# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from copy import deepcopy
from numpy import sort, zeros, sqrt, concatenate, newaxis, transpose, array, round
from numpy.random import seed
from opus_core.bayesian_melding import BayesianMelding
from opus_core.bayesian_melding import ObservedData
from opus_core.plot_functions import plot_histogram
from opus_core.misc import unique_values, write_table_to_text_file
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool

hhs_vars = {#'zone': "urbansim_parcel.zone.number_of_households",
            #'faz': "number_of_households = faz.aggregate(urbansim_parcel.zone.number_of_households)",
            #'large_area': "number_of_households = large_area.aggregate(urbansim_parcel.zone.number_of_households, intermediates=[faz])",
            #'city': "number_of_households = city.aggregate(urbansim_parcel.parcel.number_of_households)",
            #'tract10': "number_of_households = tract10.aggregate(urbansim_parcel.parcel.number_of_households)",
            'census_block_group': "number_of_households = census_block_group.aggregate(urbansim_parcel.parcel.number_of_households)",
            }
jobs_vars = {'zone': "urbansim_parcel.zone.number_of_jobs",
             'faz': "number_of_jobs = faz.aggregate(urbansim_parcel.zone.number_of_jobs)",
             'large_area': "number_of_jobs = large_area.aggregate(urbansim_parcel.zone.number_of_jobs, intermediates=[faz])",
             'city': "number_of_jobs = city.aggregate(urbansim_parcel.parcel.number_of_jobs)",
             'tract10': "number_of_jobs = tract10.aggregate(urbansim_parcel.parcel.number_of_jobs)",
            }
pop_vars = {'zone': "urbansim_parcel.zone.population",
            'faz': "population = faz.aggregate(urbansim_parcel.zone.population)",
            'large_area': "population = large_area.aggregate(urbansim_parcel.zone.population, intermediates=[faz])",
            'city': "population = city.aggregate(urbansim_parcel.parcel.population)",
            'tract10': "population = tract10.aggregate(urbansim_parcel.parcel.population)",
            }
    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # What directory contains the multiple runs'
    cache_directory = "/Users/hana/workspace/data/psrc_parcel/runs"
    cache_directory = "/Volumes/d$/opusgit/urbansim_data/data/psrc_parcel/MRuns"
    cache_directory = "/Volumes/Model Data 2/Uncertainty/urbansim_data/MRuns/baseline"
    cache_directory = "G:/Model Data 2/Uncertainty/urbansim_data/MRuns/baseline"
    #cache_directory = "/Volumes/Model Data 2/Uncertainty/urbansim_data/MRuns/tod"
    cache_directory = "G:/Model Data 2/Uncertainty/urbansim_data/MRuns/tod"
    #cache_directory = "/Volumes/D Drive TMOD3/opus/data/psrc_parcel/runs"
    # Where the observed data is stored
    observed_data_dir = "/Users/hana/workspace/data/psrc_parcel/observed_data"
    observed_data_dir = "G:/Model Data 2/Uncertainty/observed_data"
    validation_year = 2018
    run = ''
    #run = 'MR223'
    #run = 'MRr'
    #run = 10
    run_name_prefix = 'run_%s' % run
    #run_name_prefix = 'run_'
    #validation_geography = 'large_area'
    #validation_geography = 'faz'
    #validation_geography = 'city'
    #validation_geography = 'tract10'
    #validation_geography = 'zone'
    validation_geography = 'census_block_group'
    scenario = "baseline"
    scenario = "tod"
    #output_dir_base = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs/bmanal"
    output_dir_base = "/Users/hana/workspace/data/psrc_parcel/BMforTM"
    output_dir_base = "G:/Model Data 2/Uncertainty/BMforTM"
    output_directory = "%s/run%s_val%s_%s_%s" % (output_dir_base, run, validation_year, scenario, validation_geography)
    
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
 
    observed_data = ObservedData(observed_data_dir, 
                                 year=validation_year, # from what year are the observed data 
                                 storage_type='csv_storage', # in what format
                                 package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])

    known_output=[
                  {#'variable_name': "urbansim_parcel.zone.number_of_households", # What variable does the observed data correspond to
                   'variable_name': hhs_vars[validation_geography],
                   'filename': "households%s_%s" % (validation_year, validation_geography), # In what file are values of this variable
                   'transformation': "sqrt", # What transformation should be performed (can be set to None)
#                    Other arguments of the class ObservedDataOneQuantity (in bayesian_melding.py) can be set here. See its doc string.
                   #'filter': "urbansim_parcel.zone.number_of_households", 
                   'id_name': "%s_id" % validation_geography
                   },
#                    {'variable_name': "travel_data.am_single_vehicle_to_work_travel_time",
#                     'filename': "travel_times", 
#                     'transformation': "sqrt",
#                   #'filter': "urbansim_parcel.zone.number_of_households",
#                   },
                  #{#'variable_name': "urbansim_parcel.zone.number_of_jobs",
                   #'variable_name': jobs_vars[validation_geography],
                   ##'filename': "jobs2008", 
                   #'filename': "jobs%s_%s" % (validation_year, validation_geography), 
                   #'transformation': "sqrt",
                   ##'filter': "urbansim_parcel.zone.number_of_jobs",
                   #'id_name': "%s_id" % validation_geography
                   #},
                #{'variable_name': pop_vars[validation_geography],
                 #'filename': "population%s_%s" % (validation_year, validation_geography), 
                 #'transformation': "sqrt",
                 #'id_name': "%s_id" % validation_geography
                 #},
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
#                   'filename': "2008_TAZ_emp_CONFIDENTIAL", 
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
                         base_year=2014, 
                         prefix=run_name_prefix, # within 'cache_directory' filter only directories with this prefix
                         overwrite_cache_directories_file=True,
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
    
    bm.export_bm_parameters(output_directory, filename='bm_parameters')
    #bmf = BayesianMeldingFromFile("/Users/hana/bm/psrc_parcel/simulation_results/0818/2005/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'])
    
    ####
    # The code below has not been tested for a while and might not work 
    ####
    #bm.plot_boxplot_r('bm_plot.pdf', weight_threshold=0.1)
#    bm.export_weights_posterior_mean_and_variance([
#                                                   2008, 
#                                                   #2010, 2030, 2040
#                                                   ], quantity_of_interest="urbansim_parcel.zone.number_of_households",
#              directory="/Users/hana/workspace/data/psrc_parcel/runs/bmanalhhs")
#    bm.export_weights_posterior_mean_and_variance([
#                                                   2008, 
#                                                   #2010, 2030, 2040
#                                                   ], quantity_of_interest="urbansim_parcel.zone.number_of_jobs",
#              directory="/Users/hana/workspace/data/psrc_parcel/runs/bmanaljobs")
#    bm.export_weights_posterior_mean_and_variance([2020], quantity_of_interest="urbansim_parcel.zone.number_of_jobs",
#                            directory="/Users/hana/bm/psrc_parcel/simulation_results")
    from run_bm import export_quantiles
    #from run_bm_from_file import export_quant
    #output_directory = "%s/run%s_quantiles_%s" % (output_dir_base, run, validation_geography)  
    export_quantiles(bm, output_directory, years=[2040], validation_geography=validation_geography, propfac_hh = (2040 - 2014)/4., store_simulated=True, repl = 500)
    #export_quantiles(bm, output_directory, years=[2010], validation_geography=validation_geography, no_propagation=[True])
    #export_quantiles(bm, output_directory, years=[2010, 2015, 2020, 2030, 2040], validation_year=validation_year, validation_geography=validation_geography)
    #export_quantiles(bm, output_directory, years=[2040], validation_year=validation_year, validation_geography=validation_geography)
    #export_quantiles(bm, output_directory, years=[2010, 1013] + range(2015, 2026, 5), validation_year=validation_year, validation_geography=validation_geography)
    #export_quantiles(bm, output_directory, years=[2010], validation_year=validation_year, validation_geography=validation_geography)
    
def export_quantiles(bm, outdir, years=[2010, 2040], repl=10000, validation_year=2010, validation_geography='faz', 
                        propfac_hh=0.95, propfac_jobs=3.5, propfac_pop=3.9, no_propagation=[False], aggregate_to=None, 
                        store_simulated=False, **kwargs):
    header_base = ['mean', 'median', 'lower_50', 'upper_50', 'lower_80', 'upper_80', 'lower_90', 'upper_90', 'lower_95', 'upper_95']
    idcolname = {'zone': 'zone_id', 'faz': 'faz_id', 'large_area': 'large_area_id', 'city': 'city_id', 'tract10': 'tract10_id', 
                 'reggeo': 'reggeo_id', 'census_block_group': 'census_block_group_id'}
    header = {}
    for g in idcolname.keys():
        header[g] = array([idcolname[g]] + header_base)[newaxis,:]
    if aggregate_to is not None:
        header[validation_geography] = header[aggregate_to]
    #vars = {'household':hhs_vars, 'job':jobs_vars, 'population':pop_vars}
    vars = {'household':hhs_vars}
    for year in years:
        if year < validation_year:
            continue
        #for nopropag in [True, False]:
        for nopropag in no_propagation:
            if not nopropag and year == validation_year:
                continue
            #for transform in [True, False]:
            transform = True
            propfac = {}
            #for additive_prop in [True, False]:
            for additive_prop in [False]:
                if nopropag and not additive_prop:
                    continue
                if additive_prop:
                    if nopropag:
                        propfac['household'] = 0
                        propfac['job'] = 0
                        propfac['population'] = 0
                    else:
                        propfac['household'] = propfac_hh
                        propfac['job'] = propfac_jobs
                        propfac['population'] = propfac_pop
                else:
                    propfac['household'] = 1
                    propfac['job'] = 1
                    propfac['population'] = 1
                if not nopropag:
                    suffix = "_propf"
                else:
                    suffix = ""
                if not transform:
                    suffix = suffix + "_raw"
                if additive_prop and not nopropag:
                    suffix = suffix + "_add"
                seed(1)
                #for bias in [False, True]:
                for bias in [False]:
                    if bias:
                        suffix = suffix + "_bias"
                    addpropbias = not bias
                    #bmf = deepcopy(bm)
                    
                    for indicator in vars.keys():                        
                        if aggregate_to is None:
                            exact = True # calibration geography is the same as simulation target
                            bm.set_posterior(year=year, quantity_of_interest=vars[indicator][validation_geography], 
                                     additive_propagation=[addpropbias, additive_prop], 
                                     propagation_factor=[0, propfac[indicator]])
                            mean_hhs = bm.get_posterior_component_mean().mean(axis=1)
                            median = bm.get_exact_quantile(0.5, transformed_back=transform)
                            hhids = bm.get_m_ids()
                            if transform:
                                mean_hhs = mean_hhs**2
                            file_geo = validation_geography
                            if store_simulated:
                                posterior_hhs = bm.generate_posterior_distribution(year=year, quantity_of_interest=vars[indicator][validation_geography], 
                                                       replicates=repl, omit_bias=not bias, no_propagation=nopropag, additive_propagation=[addpropbias, additive_prop], 
                                                       propagation_factor=[0, propfac[indicator]], transformed_back=transform, **kwargs)
                                write_table_to_text_file(os.path.join(outdir, "simulated_values_%s" % indicator), round(concatenate((hhids[:,newaxis], bm.simulated_values), axis=1)).astype('int32'), delimiter='\t')
                                #bm.write_simulated_values(os.path.join(outdir, "simulated_values_%s" % indicator))
                                #write_table_to_text_file(os.path.join(outdir, 'ids_%s' % indicator), bm.simulated_values_ids[:,newaxis], delimiter='\t')
                        else: # aggregation
                            exact = False
                            posterior_hhs = bm.generate_posterior_distribution(year=year, quantity_of_interest=vars[indicator][validation_geography], aggregate_to=aggregate_to,
                                                   replicates=repl, omit_bias=not bias, no_propagation=nopropag, additive_propagation=[addpropbias, additive_prop], 
                                                   propagation_factor=[0, propfac[indicator]], transformed_back=transform, **kwargs)
                            mean_hhs = bm.get_quantity_from_simulated_values("mean")
                            median = bm.get_quantity_from_simulated_values("median")
                            hhids = bm.simulated_values_ids
                            file_geo = aggregate_to
                            if store_simulated:
                                bm.write_simulated_values(os.path.join(outdir, "%s_simulated_values_%s" % (aggregate_to, indicator)))
                                #write_table_to_text_file(os.path.join(outdir, '%s_ids_%s' % (aggregate_to, indicator)), bm.simulated_values_ids[:,newaxis], delimiter='\t')

                        prob80_hhs = bm.get_probability_interval(80, exact = exact, transformed_back=transform)
                        prob50_hhs = bm.get_probability_interval(50, exact = exact, transformed_back=transform)
                        prob90_hhs = bm.get_probability_interval(90, exact = exact, transformed_back=transform)
                        prob95_hhs = bm.get_probability_interval(95, exact = exact, transformed_back=transform)
                
                        write_table_to_text_file(os.path.join(outdir, '%s_%s_ci_%s%s' % (file_geo, indicator, year, suffix)), header[validation_geography])
                        write_table_to_text_file(os.path.join(outdir, '%s_%s_ci_%s%s' % (file_geo, indicator, year, suffix)), round(concatenate((hhids[:,newaxis], mean_hhs[:,newaxis], median[:,newaxis], prob50_hhs, prob80_hhs, prob90_hhs, prob95_hhs), axis=1)).astype('int32'), delimiter='\t', mode='a')

        #write_table_to_text_file(os.path.join(outdir, '%s_mu_hhs' % validation_geography), bm.get_expected_values()[0])
        #write_table_to_text_file(os.path.join(outdir, '%s_mu_jobs' % validation_geography), bm.get_expected_values()[1])
        
#                if validation_geography <> 'zone': # aggregate to large area by simulation
#                    posterior_hhs = bm.generate_posterior_distribution(year=year, quantity_of_interest="number_of_households = faz.aggregate(urbansim_parcel.zone.number_of_households)",
#                                                       replicates=repl, omit_bias=True, no_propagation=nopropag, aggregate_to='large_area', transformed_back=transform, **kwargs)
#                    prob80_hhs = bm.get_probability_interval(80, exact=False)
#                    prob50_hhs = bm.get_probability_interval(50, exact=False)
#                    prob90_hhs = bm.get_probability_interval(90, exact=False)
#                    mean_hhs = bm.get_quantity_from_simulated_values("mean")
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_hhs_ci_%s%s' % (validation_geography, year, suffix)), header_la)
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_hhs_ci_%s%s' % (validation_geography, year, suffix)), round(concatenate((bm.simulated_values_ids[:,newaxis], mean_hhs[:,newaxis], prob50_hhs, prob80_hhs, prob90_hhs), axis=1)).astype('int32'), delimiter='\t', mode='a')
#                    posterior_jobs = bm.generate_posterior_distribution(year=year, quantity_of_interest="number_of_jobs = faz.aggregate(urbansim_parcel.zone.number_of_jobs)",
#                                                       replicates=repl, omit_bias=True, no_propagation=nopropag, aggregate_to='large_area', transformed_back=transform, **kwargs)
#                    prob80_jobs = bm.get_probability_interval(80, exact=False)
#                    prob50_jobs = bm.get_probability_interval(50, exact=False)
#                    prob90_jobs = bm.get_probability_interval(90, exact=False)
#                    mean_jobs = bm.get_quantity_from_simulated_values("mean")
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_jobs_ci_%s%s' % (validation_geography, year, suffix)), header_la)
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_jobs_ci_%s%s' % (validation_geography, year, suffix)), round(concatenate((bm.simulated_values_ids[:,newaxis], mean_jobs[:,newaxis], prob50_jobs, prob80_jobs, prob90_jobs), axis=1)).astype('int32'), delimiter='\t', mode='a')
#                    posterior_pop = bm.generate_posterior_distribution(year=year, quantity_of_interest="population = faz.aggregate(urbansim_parcel.zone.population)",
#                                                       replicates=repl, omit_bias=True, no_propagation=nopropag, aggregate_to='large_area', transformed_back=transform, **kwargs)
#                    prob80_pop = bm.get_probability_interval(80, exact=False)
#                    prob50_pop = bm.get_probability_interval(50, exact=False)
#                    prob90_pop = bm.get_probability_interval(90, exact=False)
#                    mean_pop = bm.get_quantity_from_simulated_values("mean")
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_pop_ci_%s%s' % (validation_geography, year, suffix)), header_la)
#                    write_table_to_text_file(os.path.join(outdir, '%s_aggrla_pop_ci_%s%s' % (validation_geography, year, suffix)), round(concatenate((bm.simulated_values_ids[:,newaxis], mean_pop[:,newaxis], prob50_pop, prob80_pop, prob90_pop), axis=1)).astype('int32'), delimiter='\t', mode='a')

    #bm.write_values_from_multiple_runs("/Users/hana/multiple_run_values")

    #bm.write_simulated_values("/Users/hana/simulated_values")
    #bm.write_values_from_multiple_runs("/Users/hana/multiple_run_values")

    #bm.write_simulated_values(os.path.join(outdir, "simulated_values"))
    #bm.write_values_from_multiple_runs(os.path.join(outdir, "multiple_run_values"))

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
    