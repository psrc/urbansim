# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import string
import sys
import time
import re
from opus_core.logger import logger
from numpy import round_, zeros, ones, arange, logical_and, resize, concatenate, where, array
from numpy.random import seed
from scipy import ndimage
from opus_core.datasets.dataset import DatasetSubset
from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable_name import VariableName
from psrc_parcel.travel_model_input_file_writer import TravelModelInputFileWriter as PSRCTravelModelInputFileWriter
from opus_core.misc import safe_array_divide
from opus_core.sampling_toolbox import sample_replace
from urbansim.lottery_choices import lottery_choices

class TravelModelInputFileWriter(PSRCTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. 
        It simulates number of households and number of jobs from a posterior distribution of a bayesian melding analysis.
    """

    zone_variables_to_precompute = ['number_of_non_home_based_jobs = zone.aggregate(urbansim.job.is_non_home_based_job)',
                        'number_of_nhb_workers = zone.aggregate(urbansim_parcel.household.number_of_non_home_based_workers_with_job, [building, parcel])'
                            ]
    variables_to_scale = {
        'household': {
            "hhs_of_first_quarter" : None,
            "hhs_of_second_quarter": None,
            "hhs_of_third_quarter": None,
            "hhs_of_fourth_quarter": None,
                    },
        'job': {
            'number_of_non_home_based_jobs': None
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
    
    log_file_name = 'run_travel_model_bm.log'
    
    def run(self, current_year_emme2_dir, current_year, dataset_pool, config=None):
        self._do_setup(current_year, dataset_pool, config)
        PSRCTravelModelInputFileWriter.run(self, current_year_emme2_dir, current_year, dataset_pool, config)
        
    def _do_setup(self, current_year, dataset_pool, config=None, enable_file_logging=True):
        self.configuration = config
        self.year = current_year
        self.dataset_pool = dataset_pool
        self.simulated_values = {}
        if enable_file_logging:
            logdir = os.path.join(config['cache_directory'], str(current_year+1))
            if not os.path.exists(logdir):
                os.makedirs('%s' % logdir)
            log_file = os.path.join(logdir, self.log_file_name)
            logger.enable_file_logging(log_file)
        if config is not None and 'seed' in config.keys():
            seed(config['seed'])
            logger.log_status('seed: %s' % config['seed'])

        
    def get_variables_list(self, dataset_pool):
        self.full_variable_list = PSRCTravelModelInputFileWriter.get_variables_list(self, dataset_pool)
        return self.zone_variables_to_precompute + self.full_variable_list[0:8] + self.full_variable_list[20:24] # some job variables removed, since they are computed within _determine_simulated_values
        
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        self.generate_travel_model_input(zone_set)
        PSRCTravelModelInputFileWriter._write_to_file(self, zone_set, self.full_variable_list, tm_input_file)

    def _write_workplaces_to_files(self, person_set, tm_input_files):
        new_person_set = self.generate_workplaces(person_set)
        return PSRCTravelModelInputFileWriter._write_workplaces_to_files(self, new_person_set, tm_input_files)
        
    def generate_travel_model_input(self, zone_set):
        self.bm_generate_from_posterior(zone_set)
        
    def _get_value_for_zone(self, zone_id, zone_set, variable_name):
        var_alias = VariableName(variable_name).get_alias()
        if  var_alias in self.simulated_values.keys():
            index = zone_set.get_id_index(zone_id)
            return self.simulated_values[var_alias][index]
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
            #logger.log_status('Current number of %ss' % dataset_name)
            #logger.log_status(number_of_agents)
            nvars = len(self.variables_to_scale[dataset_name].keys())
            for var in self.variables_to_scale[dataset_name].keys():
                self.variables_to_scale[dataset_name][var] = safe_array_divide(zone_set.get_attribute(var), number_of_agents,
                                                                               return_value_if_denominator_is_zero=1.0/float(nvars))
            
    def _determine_simulated_values(self, zone_set, file):
        bm_module, bm_class = self.configuration['travel_model_configuration'].get('bm_module_class_pair', 
                                                                                   ('opus_core.bayesian_melding', 
                                                                                        'BayesianMeldingFromFile'))
        exec('from %s import %s' % (bm_module, bm_class))
        post_module, post_class = self.configuration['travel_model_configuration'].get('bm_posterior_procedure', 
                                                                                   ('opus_core.bm_normal_posterior', 
                                                                                        'bm_normal_posterior'))
        exec('from %s import %s' % (post_module, post_class))
        
        bm = eval('%s(file)' % bm_class)
        variables_to_compute = [var for var in bm.get_variable_names() if VariableName(var).get_alias() not in zone_set.get_primary_attribute_names()]
        if len(variables_to_compute) > 0:
            zone_set.compute_variables(variables_to_compute, dataset_pool=self.dataset_pool)
        zone_ids = zone_set.get_id_attribute()
        
        # simulate households
        dataset_name = 'household'
        bmvar = get_variables_for_number_of_agents(dataset_name, bm.get_variable_names())[0] # this should be a list with one element ('number_of_households')
        bm.set_posterior(self.year, bmvar, zone_set.get_attribute(bmvar), zone_ids, transformation_pair = ("sqrt", "**2"))
        n = eval('%s().run(bm, replicates=1)' % post_class)
        simulated_number_of_agents = n.ravel()*n.ravel()
        logger.log_status('Simulated number of %ss' % dataset_name)
        #logger.log_status(round_(simulated_number_of_agents[0:50]))
        scale_to_ct = False
        if self.configuration['travel_model_configuration'].get('scale_to_control_totals', False):
            control_totals = self.configuration['travel_model_configuration'].get('control_totals')
            household_control_total = control_totals['households']
            job_control_total = control_totals['jobs']
            scale_to_ct = True
            simulated_number_of_agents = simulated_number_of_agents/float(simulated_number_of_agents.sum()) * household_control_total
        for var, ratios in self.variables_to_scale[dataset_name].iteritems():
            var_alias = VariableName(var).get_alias()
            self.simulated_values[var_alias] = zeros(zone_set.size())
            self.simulated_values[var_alias][zone_set.get_id_index(bm.get_m_ids())] = (round_(simulated_number_of_agents*ratios)).astype(self.simulated_values[var_alias].dtype)
            #logger.log_status(var)
            #logger.log_status(self.simulated_values[var_alias])
            logger.log_status('Total number of %s: %s' % (var, self.simulated_values[var_alias].sum()))
            
        # simulate jobs
        dataset_name = 'job'
        logger.log_status('Generated values of bm variables for %ss:' % dataset_name)
        bmvars = get_variables_for_number_of_agents(dataset_name, bm.get_variable_names())
        self.total_number_of_jobs = zeros(zone_set.size(), dtype='int32')
        for bmvar in bmvars:
            bm.set_posterior(self.year, bmvar, zone_set.get_attribute(bmvar), zone_ids, transformation_pair = ("sqrt", "**2"))
            n = eval('%s().run(bm, replicates=1)' % post_class)
            simulated_number_of_agents = n.ravel()*n.ravel()
            if scale_to_ct:
                for key, ct in job_control_total.iteritems():
                    if bmvar.endswith(key):
                        simulated_number_of_agents = simulated_number_of_agents/float(simulated_number_of_agents.sum()) * ct
                        break
            #logger.log_status(bmvar)
            #logger.log_status(zone_set.get_attribute(bmvar))
            logger.log_status('Total number of %s: %s' % (bmvar, simulated_number_of_agents.sum()))
            zone_set.modify_attribute(bmvar, round_(simulated_number_of_agents))
            self.total_number_of_jobs = self.total_number_of_jobs + simulated_number_of_agents
        zone_set.compute_variables(self.variables_for_direct_matching[dataset_name], dataset_pool=self.dataset_pool)
        #logger.log_status('Simulated values of bm variables for %ss:' % dataset_name)
        for var in self.variables_for_direct_matching[dataset_name]:
            var_alias = VariableName(var).get_alias()
            self.simulated_values[var_alias] = zone_set.get_attribute(var)
            #logger.log_status(var)
            #logger.log_status(self.simulated_values[var])
         
    def generate_workplaces(self, person_set):   
        """ assign workers to jobs separately for each income category"""
        zone_set = self.dataset_pool.get_dataset("zone")
        zone_ids = zone_set.get_id_attribute()
        persons_job_zone_ids = person_set.get_attribute('job_zone_id')
        persons_zone_ids = person_set.get_attribute('zone_id')
        households = self.dataset_pool.get_dataset('household')
        hh_categories = {
                    1: "hhs_of_first_quarter",
                    2: "hhs_of_second_quarter",
                    3: "hhs_of_third_quarter",
                    4: "hhs_of_fourth_quarter"
            }
        number_of_nhb_jobs = round_(self.total_number_of_jobs * self.variables_to_scale['job']['number_of_non_home_based_jobs'])
        current_number_of_nhb_workers = households.compute_variables(['urbansim_parcel.household.number_of_non_home_based_workers'], dataset_pool=self.dataset_pool)
        sim_number_of_nhb_workers = {}
        resulting_workers = {
                             'zone_id': array([], dtype='int32'),
                             'job_zone_id': array([], dtype='int32'),
                             'income_group_1': array([], dtype='int32'),
                             'income_group_2': array([], dtype='int32'),
                             'income_group_3': array([], dtype='int32'),
                             'income_group_4': array([], dtype='int32')
                             }
        hhs_zone_ids = households.get_attribute('zone_id')
        # iterate over income categories
        for category in range(1,5):
            logger.log_status('Income category %s' % category)
            is_hhs_category = households.get_attribute('is_income_group_%s' % category)
            hhs_category_idx = where(is_hhs_category)[0]
            person_is_in_category = logical_and(person_set.get_attribute("is_placed_non_home_based_worker_with_job"), 
                                                   person_set.get_attribute("income_group_%s" % category))
            sim_number_of_households = self.simulated_values[hh_categories[category]]
            # iterate over zones
            for izone in arange(zone_set.size()):
                if sim_number_of_households[izone] <= 0:
                    continue
                logger.log_status('Zone %s' % zone_ids[izone])
                # sample a number of nhb workers from the empirical distribution of the category and zone
                hhs_of_this_category_and_zone_idx = where(logical_and(is_hhs_category, hhs_zone_ids == zone_ids[izone]))[0]
                if (hhs_of_this_category_and_zone_idx.size <= 0) or (hhs_of_this_category_and_zone_idx.size < 10 and sim_number_of_households[izone] > 100):
                    # if there is not enough observations, sample from the empirical distribution of the whole category
                    logger.log_status(
                        'Not enough observations to sample from. Sampled from distribution of all zones of this category. (%s observations, %s samples)' % (
                                                                                hhs_of_this_category_and_zone_idx.size, sim_number_of_households[izone]))
                    hhs_of_this_category_and_zone_idx = hhs_category_idx
                    persons_considered = person_is_in_category
                else:
                    persons_considered = logical_and(person_is_in_category, persons_zone_ids == zone_ids[izone])
                draw = sample_replace(hhs_of_this_category_and_zone_idx, sim_number_of_households[izone])
                sim_number_of_nhb_workers[category] = current_number_of_nhb_workers[draw].sum()
                if sim_number_of_nhb_workers[category] <= 0:
                    continue
                job_distribution = array(ndimage.sum(persons_considered, labels=persons_job_zone_ids, index = zone_ids))
                job_distribution = job_distribution / float(job_distribution.sum())
                # place workers to jobs with the lottery alg.; the probability is proportional to number of nhb workers
                # in each zone
                zone_idx = self.place_workers(job_distribution, number_of_nhb_jobs, sim_number_of_nhb_workers[category])
                valid_zone_idx = zone_idx[zone_idx >=0]
                resulting_workers['zone_id'] = concatenate((resulting_workers['zone_id'], 
                                                              resize(array([zone_ids[izone]]), (valid_zone_idx.size,))))
                resulting_workers['job_zone_id'] = concatenate((resulting_workers['job_zone_id'], zone_ids[valid_zone_idx]))
                resulting_workers['income_group_%s' % category] = concatenate((resulting_workers['income_group_%s' % category], 
                                                                               ones(valid_zone_idx.size, dtype='bool8')))
                for g in range(1,5):
                    if g <> category:
                        resulting_workers['income_group_%s' % g] = concatenate((resulting_workers['income_group_%s' % g], 
                                                                               zeros(valid_zone_idx.size, dtype='bool8')))
                # update capacity
                workers_zones_in_this_iter = array(ndimage.sum(ones(valid_zone_idx.size, dtype='bool8'), labels=zone_ids[valid_zone_idx], index=zone_ids))
                number_of_nhb_jobs = number_of_nhb_jobs - workers_zones_in_this_iter
                if number_of_nhb_jobs.sum() <=0:
                    break
                
        resulting_workers["is_placed_non_home_based_worker_with_job"] = ones(resulting_workers['zone_id'].size, dtype='bool8')
        # create new person set
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='simulated_persons',
                            table_data=resulting_workers)
        new_person_set = Dataset(in_storage=storage, in_table_name='simulated_persons', id_name=[], dataset_name='simulated_person')
        return new_person_set
                
    
    def place_workers(self, probability, capacity, n):
        resources = Resources({'capacity': capacity, "lottery_max_iterations": 10})
        probs = resize(probability, (n, probability.size))
        logger.log_status('Place %s workers into %s jobs.' % (n, (capacity*(probability > 0)).sum()))
        return lottery_choices().run(probs, resources)
                
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
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
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
        
        tmiw._do_setup(2010, dataset_pool, config={'travel_model_configuration': {'bm_distribution_file': temp_file[1]}}, enable_file_logging=False)
        zones.compute_variables(tmiw.variables_to_scale['household'].keys(), dataset_pool = tmiw.dataset_pool)

        tmiw.bm_generate_from_posterior(zones)
        os.remove(temp_file[1])
        
if __name__ == '__main__':
    opus_unittest.main()
