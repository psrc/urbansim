#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os
import string
import sys
import time
from opus_core.logger import logger
from numpy import round_, zeros
from opus_core.datasets.dataset import DatasetSubset
from opus_core.variables.variable_name import VariableName
from psrc.travel_model_input_file_writer import TravelModelInputFileWriter as PSRCTravelModelInputFileWriter
from opus_core.bayesian_melding import BayesianMeldingFromFile
from opus_core.bm_normal_posterior import bm_normal_posterior

class TravelModelInputFileWriter(PSRCTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. """
    
    def run(self, current_year_emme2_dir, current_year, dataset_pool, config=None):
        self.configuration = config
        self.year = current_year
        self.dataset_pool = dataset_pool
        self.simulated_values = {}
        self.variables = {'household': {
            "hhs_of_first_quarter" : None,
            "hhs_of_second_quarter": None,
            "hhs_of_third_quarter": None,
            "hhs_of_fourth_quarter": None,
                    },
                'job': {
            "density_1_retail_jobs": None,
            "density_2_retail_jobs": None,
            "density_3_retail_jobs": None,
            "density_1_fires_jobs": None,
            "density_2_fires_jobs": None,
            "density_3_fires_jobs": None,
            "density_1_gov_jobs": None,
            "density_2_gov_jobs": None,
            "density_3_gov_jobs": None,
            "edu_jobs": None,
            "wtcu_jobs": None,
            "manu_jobs": None,  
                     }
                }

        PSRCTravelModelInputFileWriter.run(self, current_year_emme2_dir, current_year, dataset_pool, config)
        
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        self.bm_generate_from_posterior(zone_set)
        PSRCTravelModelInputFileWriter._write_to_file(self, zone_set, variables_list, tm_input_file)

    def _get_value_for_zone(self, zone_id, zone_set, variable_name):
        if variable_name in self.simulated_values.keys():
            index = zone_set.get_id_index(zone_id)
            return self.simulated_values[variable_name][index]
        PSRCTravelModelInputFileWriter._get_value_for_zone(self, zone_id, zone_set, variable_name)

    def bm_generate_from_posterior(self, zone_set):
        bmconfig = self.configuration['travel_model_configuration'].get('bm_distribution_files',None)
        if bmconfig is None:
            raise StandardError, "'bm_distribution_files' must be given."
        if self.year not in bmconfig.keys():
            raise StandardError, "Year %s not contained in 'bm_distribution_files'."
        for dataset in ['job', 'household']:
            file = bmconfig[self.year][dataset]
            self._determine_current_share(dataset, zone_set)
            self._determine_simulated_values(dataset, zone_set, file)
        
    def _determine_current_share(self, dataset_name, zone_set):
        number_of_agents = zone_set.compute_variables(['zone.number_of_agents(%s)' % dataset_name], dataset_pool=self.dataset_pool).astype('float32')
        for var in self.variables[dataset_name].keys():
            self.variables[dataset_name][var] = zone_set.get_attribute(var)/number_of_agents
            
    def _determine_simulated_values(self, dataset_name, zone_set, file):
        bm = BayesianMeldingFromFile(file)
        n = bm_normal_posterior().run(bm, replicates=1)
        for var, ratios in self.variables[dataset_name].iteritems():
            self.simulated_values[var] = zeros(zone_set.size(), dtype='int32')
            self.simulated_values[var][zone_set.get_id_index(bm.get_m_ids())] = (round_(n.ravel()*n.ravel()*ratios)).astype('int32')
            