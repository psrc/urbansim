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
from numpy import sort
from opus_core.bayesian_melding import BayesianMelding
from opus_core.plot_functions import plot_histogram
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.faz_dataset import FazDataset
from urbansim.datasets.large_area_dataset import LargeAreaDataset
from opus_core.session_configuration import SessionConfiguration

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    # set true_data_cache if the true data are stored in a cache (in the same way as an urbansim cache)
    #true_data_cache = "/scratch/urbbuild/urbansim_cache/psrc/uncertainty/run_1364.2006_12_01_10_42"

    # in what directory is the file 'cache_directories'
    cache_directory = "/home/hana/urbansim_cache/psrc/parcel/run_3904.2007_10_19_15_01"

    # This is needed only if one of the runs was scaled, e.g. run on reduced set of gridcells. 
    # It gives the directory of the base year full set, in order to scale back.
#    scaling = {1: "/scratch/urbbuild/urbansim_cache/psrc/cache_source_zone"}

    # where the true data (on a zone level) is stored in a table format 
    #true_data_dir = "/Users/hana/data/"
    true_data_dir = "/home/hana/urbansim_cache/psrc/data"

    true_data_file_name = "PSRC2005TAZData" # the physical file should have the ending '.tab'

    in_storage = StorageFactory().get_storage('tab_storage',
                                              storage_location = true_data_dir)
    zones = ZoneDataset(in_storage=in_storage, in_table_name=true_data_file_name)
    
    flt_storage = StorageFactory().get_storage('flt_storage',
                                              storage_location = cache_directory + "/2000")
    fazes = FazDataset(in_storage=flt_storage, in_table_name='fazes')
    large_areas = LargeAreaDataset(in_storage=flt_storage, in_table_name='large_areas')

    bm = BayesianMelding(cache_directory, 
                         #cache_with_true_data=true_data_cache, 
                         datasets_with_true_data={'zone':zones, 'faz':fazes, 'large_area': large_areas},
                         year_with_true_data=2002,
                         known_output=["urbansim_parcel.zone.number_of_households", 
                        #"urbansim_parcel.zone.number_of_jobs"
                        ], 
                         transformation = 'sqrt', base_year=2000, 
                         #scaling_parents = scaling,
                         dataset_package='urbansim')
    weights = bm.compute_weights()
    print weights

#    posterior = bm.generate_posterior_distribution(year=2010, quantity_of_interest="urbansim.zone.number_of_households",
#                                                   use_bias_and_variance_from = "urbansim.zone.number_of_households", 
#                                                   replicates=1000)

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