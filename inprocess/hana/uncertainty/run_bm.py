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
from opus_core.bayesian_melding import ObservedData
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
    #cache_directory = "/home/hana/urbansim_cache/psrc/parcel/run_3904.2007_10_19_15_01"
    cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/run_3914.2007_10_19_18_55"
    # This is needed only if one of the runs was scaled, e.g. run on reduced set of gridcells. 
    # It gives the directory of the base year full set, in order to scale back.
#    scaling = {1: "/scratch/urbbuild/urbansim_cache/psrc/cache_source_zone"}

    # where the true data (on a zone level) is stored in a table format 
    observed_data_dir = "/Users/hana/bm/observed_data/"

    observed_data = ObservedData(observed_data_dir, 2002, 'tab_storage', 
                                 package_order=['urbansim_parcel', 'urbansim', 'opus_core'])

    known_output=[{'variable_name': "urbansim_parcel.zone.number_of_households",
                   'filename': "PSRC2005TAZData", 
                   'transformation': "sqrt",
                   },
                  {'variable_name': "urbansim_parcel.zone.number_of_jobs",
                   'filename': "PSRC2005TAZData", 
                   'transformation': "sqrt",
                   },
#                  {'variable_name': "urbansim_parcel.faz_x_land_use_type.total_value_per_sqft",
#                   'filename': "avg_total_value_per_unit_by_faz", 
#                   'transformation': "log",
#                   'filter': 'faz_x_land_use_type_flatten.total_value_per_sqft > 0',
#                   "id_name":  ["faz_id", "land_use_type_id"]
#                   },
                  {'variable_name': "urbansim_parcel.large_area_x_land_use_type.total_value_per_sqft",
                   'filename': "avg_total_value_per_unit_by_la", 
                   'transformation': "log",
                   #'filter': 'faz_x_land_use_type_flatten.total_value_per_sqft > 0',
                   "id_name":  ["large_area_id", "land_use_type_id"]
                   }
                  ]
                  
    for quantity in known_output:
        observed_data.add_quantity(**quantity)
        
    bm = BayesianMelding(cache_directory, 
                         observed_data,                        
                         base_year=2000, 
                         #scaling_parents = scaling,
                         package_order=['urbansim_parcel', 'urbansim', 'opus_core'])
    weights = bm.compute_weights()
    print weights

    posterior = bm.generate_posterior_distribution(year=2005, quantity_of_interest="urbansim_parcel.zone.number_of_households",
                                                   replicates=10)

    bm.write_simulated_values("/Users/hana/simulated_values")
    bm.write_values_from_multiple_runs("/Users/hana/multiple_run_values")
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