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
import re
from opus_core.logger import logger
from numpy import round_, zeros
from opus_core.datasets.dataset import DatasetSubset
from opus_core.variables.variable_name import VariableName
from psrc.travel_model_input_file_writer import TravelModelInputFileWriter as PSRCTravelModelInputFileWriter
from opus_core.bayesian_melding import BayesianMeldingFromFile
from opus_core.bm_normal_posterior import bm_normal_posterior
from opus_core.misc import safe_array_divide

class TravelModelInputFileWriter(PSRCTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. """

    variables_to_scale = {
        'household': {
            "hhs_of_first_quarter" : None,
            "hhs_of_second_quarter": None,
            "hhs_of_third_quarter": None,
            "hhs_of_fourth_quarter": None,
                    }
        }
    variables_for_direct_matching = {
          'job': [
            "density_1_retail_jobs = (zone.density==1).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_retail", #109
            "density_2_retail_jobs = (zone.density==2).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_retail", #110
            "density_3_retail_jobs = (zone.density==3).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_retail", #111
            "density_1_fires_jobs = (zone.density==1).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_fires",   #112
            "density_2_fires_jobs = (zone.density==2).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_fires",   #113
            "density_3_fires_jobs = (zone.density==3).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_fires",   #114
            "density_1_gov_jobs = (zone.density==1).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_gov",       #115
            "density_2_gov_jobs = (zone.density==2).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_gov",       #116
            "density_3_gov_jobs = (zone.density==3).astype(float32) * urbansim_parcel.zone.number_of_jobs_of_sector_group_gov",       #117 
            "edu_jobs = urbansim_parcel.zone.number_of_jobs_of_sector_group_edu",     #118
            "wtcu_jobs = urbansim_parcel.zone.number_of_jobs_of_sector_group_wtcu",   #119
            "manu_jobs = urbansim_parcel.zone.number_of_jobs_of_sector_group_manu",   #120
                ]
        }
    
    def run(self, current_year_emme2_dir, current_year, dataset_pool, config=None):
        self.configuration = config
        self.year = current_year
        self.dataset_pool = dataset_pool
        self.simulated_values = {}
        logdir = os.path.join(config['cache_directory'], str(current_year+1))
        if not os.path.exists(logdir):
            os.makedirs('%s' % logdir)
        log_file = os.path.join(logdir, 'run_travel_model_bm.log')
        
        logger.enable_file_logging(log_file)
        PSRCTravelModelInputFileWriter.run(self, current_year_emme2_dir, current_year, dataset_pool, config)
        
    def get_variables_list(self, dataset_pool):
        self.full_variable_list = PSRCTravelModelInputFileWriter.get_variables_list(self, dataset_pool)
        return self.full_variable_list[0:8] + self.full_variable_list[20:24] # jobs variablees removed, since they are computed within _determine_simulated_values
        
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        self.bm_generate_from_posterior(zone_set)
        PSRCTravelModelInputFileWriter._write_to_file(self, zone_set, self.full_variable_list, tm_input_file)

    def _get_value_for_zone(self, zone_id, zone_set, variable_name):
        if variable_name in self.simulated_values.keys():
            index = zone_set.get_id_index(zone_id)
            return self.simulated_values[variable_name][index]
        return PSRCTravelModelInputFileWriter._get_value_for_zone(self, zone_id, zone_set, variable_name)

    def bm_generate_from_posterior(self, zone_set):
        bmfile = self.configuration['travel_model_configuration'].get('bm_distribution_file', None)
        if bmfile is None:
            raise StandardError, "'bm_distribution_file' must be given."
        self._determine_current_share(zone_set)
        self._determine_simulated_values(zone_set, bmfile)
        
    def _determine_current_share(self, zone_set):
        for dataset_name in self.variables_to_scale.keys():
            number_of_agents = zone_set.compute_variables(['zone.number_of_agents(%s)' % dataset_name], dataset_pool=self.dataset_pool).astype('float32')
            logger.log_status('Current number of %ss' % dataset_name)
            logger.log_status(number_of_agents)
            for var in self.variables_to_scale[dataset_name].keys():
                self.variables_to_scale[dataset_name][var] = safe_array_divide(zone_set.get_attribute(var), number_of_agents)
            
    def _determine_simulated_values(self, zone_set, file):
        bm = BayesianMeldingFromFile(file)
        variables_to_compute = [var for var in bm.get_variable_names() if VariableName(var).get_alias() not in zone_set.get_primary_attribute_names()]
        if len(variables_to_compute) > 0:
            zone_set.compute_variables(variables_to_compute, dataset_pool=self.dataset_pool)
        zone_ids = zone_set.get_id_attribute()
        for dataset_name in self.variables_to_scale.keys():
            bmvar = get_variables_for_number_of_agents(dataset_name, bm.get_variable_names())[0] # this should be a list with one element ('number_of_households')
            bm.set_posterior(self.year, bmvar, zone_set.get_attribute(bmvar), zone_ids, transformation_pair = ("sqrt", "**2"))
            n = bm_normal_posterior().run(bm, replicates=1)
            simulated_number_of_agents = n.ravel()*n.ravel()
            logger.log_status('Simulated number of %ss' % dataset_name)
            logger.log_status(round_(simulated_number_of_agents))
            for var, ratios in self.variables_to_scale[dataset_name].iteritems():
                self.simulated_values[var] = zeros(zone_set.size())
                self.simulated_values[var][zone_set.get_id_index(bm.get_m_ids())] = (round_(simulated_number_of_agents*ratios)).astype(self.simulated_values[var].dtype)
                logger.log_status(var)
                logger.log_status(self.simulated_values[var])
            
        for dataset_name in self.variables_for_direct_matching.keys():
            logger.log_status('Current values of bm variables for %ss:' % dataset_name)
            bmvars = get_variables_for_number_of_agents(dataset_name, bm.get_variable_names())
            for bmvar in bmvars:
                bm.set_posterior(self.year, bmvar, zone_set.get_attribute(bmvar), zone_ids, transformation_pair = ("sqrt", "**2"))
                n = bm_normal_posterior().run(bm, replicates=1)
                simulated_number_of_agents = n.ravel()*n.ravel()
                logger.log_status(bmvar)
                logger.log_status(zone_set.get_attribute(bmvar))
                zone_set.modify_attribute(bmvar, round_(simulated_number_of_agents))
            zone_set.compute_variables(self.variables_for_direct_matching[dataset_name], dataset_pool=self.dataset_pool)
            logger.log_status('Simulated values of bm variables for %ss:' % dataset_name)
            for var in self.variables_for_direct_matching[dataset_name]:
                self.simulated_values[var] = zone_set.get_attribute(var)
                logger.log_status(var)
                logger.log_status(self.simulated_values[var])
                
def get_variables_for_number_of_agents(agent_name, variables):
    return [var for var in variables if re.compile("number_of_%s" % agent_name).search(var)]
            
from opus_core.tests import opus_unittest
import tempfile
from numpy import array, arange
from opus_core.misc import write_to_text_file
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.zone_dataset import ZoneDataset
from opus_core.datasets.dataset_pool import DatasetPool

class TestTMInputWriter(opus_unittest.OpusTestCase):
    def test_bm_simulation(self):
        # prepare file with the bm parameters
        temp_file = tempfile.mkstemp(prefix='opus_tmp')
        write_to_text_file(temp_file[1], array([2000, 2005]), delimiter=' ')
        
        write_to_text_file(temp_file[1], array(["urbansim_parcel.zone.number_of_households"]), mode='a')
        write_to_text_file(temp_file[1], array([-0.1, 2.]), mode='a', delimiter=' ')
        
        write_to_text_file(temp_file[1], array(["number_of_jobs_of_sector_group_retail = zone.aggregate(urbansim_parcel.building.number_of_jobs_of_sector_group_retail)"]), mode='a')
        write_to_text_file(temp_file[1], array([0, 1.3]), mode='a', delimiter=' ')
        
        write_to_text_file(temp_file[1], array(["number_of_jobs_of_sector_group_manu = zone.aggregate(urbansim_parcel.building.number_of_jobs_of_sector_group_manu)"]), mode='a')
        write_to_text_file(temp_file[1], array([-1.9, 18.4]), mode='a', delimiter=' ')
        
        high_income = array([5, 0, 5, 1, 0, 60, 10, 7, 0, 0])
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name = "zones",
            table_data = {
                "zone_id": arange(10)+1,
                "number_of_jobs_of_sector_group_retail": array([100, 2000, 0, 40, 23, 35, 0, 1, 900, 879]),
                "number_of_jobs_of_sector_group_manu": array([0, 0, 2030, 20, 421, 0, 3, 97, 600, 0]),
                "density": array([1,1,1,1,1,2,2,2,2,2]),
                }
            )
        storage.write_table(
            table_name = "households",
            table_data = {
                "household_id": arange(221)+1,
                "zone_id": array(10*[1] + 25*[3] + [4] + 100*[6] + 30*[7] + 43*[8] + 2*[9] + 10*[10]),
                "is_high_income": array(5*[True] + 5*[False] + 5*[True] + 20*[False] + [True] + 60*[True]+ 40*[False] + 10*[True] + 20*[False] + 7*[True] + 36*[False] + 2*[False] + 10*[False])
                }
            )
        zones = ZoneDataset(in_storage=storage)
        
        tmiw = TravelModelInputFileWriter()
        
        tmiw.variables_to_scale = {
            'household': {
                    "high_income = zone.aggregate(household.is_high_income)": None,
                    "low_income = zone.aggregate(numpy.logical_not(household.is_high_income))": None,
                        }
                          }
        tmiw.variables_for_direct_matching = {
          'job': [
                  "retail1 = (zone.density==1) * zone.number_of_jobs_of_sector_group_retail",
                  "retail2 = (zone.density==2) * zone.number_of_jobs_of_sector_group_retail",
                  "manu = zone.number_of_jobs_of_sector_group_manu"
                  ]
          }
        tmiw.dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        tmiw.year = 2010
        tmiw.simulated_values = {}
        zones.compute_variables(tmiw.variables_to_scale['household'].keys(), dataset_pool = tmiw.dataset_pool)
        tmiw.configuration = {'travel_model_configuration': {'bm_distribution_file': temp_file[1]}}
        
        tmiw.bm_generate_from_posterior(zones)
        os.remove(temp_file[1])
        
if __name__ == '__main__':
    opus_unittest.main()