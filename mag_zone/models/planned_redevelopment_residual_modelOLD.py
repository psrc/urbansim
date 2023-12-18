# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.misc import DebugPrinter
from opus_core.datasets.dataset import DatasetSubset
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.logger import logger
from numpy import where, bincount, unique, around, concatenate, zeros
from prettytable import PrettyTable

class PlannedRedevelopmentResidualModel(Model):
    """

    Model development in progress.  Please do not use.
    
    If you have questions, contact Jesse Ayers at MAG:  jayers@azmag.gov
    
    """

    model_name = 'Planned Redevelopment Residual Model'
    model_short_name = 'PRRM'

    def __init__(self, debuglevel=1):
        self.debug = DebugPrinter(debuglevel)
        self.debuglevel = debuglevel

    def run(self, year=None, dataset_pool=None):

        # Get current simulation year
        if year is None:
            simulation_year = SimulationState().get_current_time()
        else:
            simulation_year = year

        # Get the dataset pool
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()
            self.dataset_pool = dataset_pool
        else:
            dataset_pool = dataset_pool
            self.dataset_pool = dataset_pool

        # get the buildings dataset
        self.buildings_dataset = dataset_pool.get_dataset('building')

        # compute variables
        percent_non_residential_sqft_built = \
            self.buildings_dataset.compute_variables("percent_non_residential_sqft_built = safe_array_divide(building.non_residential_sqft, building.non_residential_sqft_capacity)")
        percent_dus_built = \
            self.buildings_dataset.compute_variables("percent_dus_built = safe_array_divide(building.residential_units, building.residential_units_capacity)")
        non_residential_sqft_land_built = \
            self.buildings_dataset.compute_variables("non_residential_sqft_land_built = building.percent_non_residential_sqft_built * building.land_area")
        dus_land_built = self.buildings_dataset.compute_variables("dus_land_built = building.percent_dus_built * building.land_area", dataset_pool=dataset_pool)

        # get an index of the redevelopment building records
        # if none, exit
        try:
            redevelopment_buildings_index = where(self.buildings_dataset.get_attribute('redevelopment_building_id')>0)[0]
        except:
            logger.log_warning('\n*** The buidlings dataset has no attribute "redevelopment_building_id."***\n*** The Planned Redevelopment Residuals Model will not run. ***\n')
            return

        # get an array of the actual redevelopment building record ids
        redevelopment_buildings_ids = self.buildings_dataset.get_attribute('redevelopment_building_id')[redevelopment_buildings_index]

        # check for redevelopment records, if none, exit
        if where(redevelopment_buildings_ids>-1)[0].size < 1:
            logger.log_warning('\n*** The buildings dataset contains no redevelopment records.***\n*** The Planned Redevelopment Residuals Model will not run. ***\n')
            return

        # get land built for non-residential sqft and residential units for only redevelopment buildings
        non_residential_sqft_land_built_subset = non_residential_sqft_land_built[redevelopment_buildings_index]
        dus_land_built_subset = dus_land_built[redevelopment_buildings_index]
        # sum up the land built over the redevelopment buildings (uses numpy bitcount)
        non_residential_sqft_land_built_subset_sum = bincount(redevelopment_buildings_ids,non_residential_sqft_land_built_subset)
        dus_land_built_subset_sum = bincount(redevelopment_buildings_ids,dus_land_built_subset)
        # sum up total land built on redevelopment buildings
        total_land_redeveloped = non_residential_sqft_land_built_subset_sum + dus_land_built_subset_sum
        # get unique redevelopment ids
        unique_redevelopment_building_ids = unique(redevelopment_buildings_ids)
        # compute pct redeveloped
        total_percent_land_redeveloped = total_land_redeveloped[unique_redevelopment_building_ids] \
                                            / self.buildings_dataset.get_attribute_by_id('land_area',unique_redevelopment_building_ids)

        # compute non-residential sqft and units to remove
        try:
            total_dus_to_remove = around(self.buildings_dataset.get_attribute_by_id('base_year_residential_units',unique_redevelopment_building_ids) \
                                        * total_percent_land_redeveloped).astype('int')
        except:
            logger.log_error('\n***\n*** The required column "base_year_residential_units" is not present on the buildings dataset.\n***Exiting Redevelopment Model\n***')
            return
        total_dus_present = self.buildings_dataset.get_attribute_by_id('residential_units',unique_redevelopment_building_ids).astype('int')
        total_dus_base = self.buildings_dataset.get_attribute_by_id('base_year_residential_units',unique_redevelopment_building_ids).astype('int')
        total_base_dus_min_remove = total_dus_base - total_dus_to_remove
        
        total_dus_to_remove_this_year = total_dus_present - total_base_dus_min_remove
        total_dus_to_remove_this_year[total_dus_to_remove_this_year<0] = 0

        try:
            total_non_residential_sqft_to_remove = around(self.buildings_dataset.get_attribute_by_id('base_year_non_residential_sqft',unique_redevelopment_building_ids) \
                                        * total_percent_land_redeveloped).astype('int')
        except:
            logger.log_error('\n***\n*** The required column "base_year_non_residential_sqft" is not present on the buildings dataset.\n*** Exiting Redevelopment Model\n***')
            return        
        total_nonres_sqft_present = self.buildings_dataset.get_attribute_by_id('non_residential_sqft',unique_redevelopment_building_ids).astype('int')
        total_nonres_sqft_base = self.buildings_dataset.get_attribute_by_id('base_year_non_residential_sqft',unique_redevelopment_building_ids).astype('int')
        total_base_sqft_min_remove = total_nonres_sqft_base - total_non_residential_sqft_to_remove

        total_non_residential_sqft_to_remove_this_year = total_nonres_sqft_present - total_base_sqft_min_remove
        total_non_residential_sqft_to_remove_this_year[total_non_residential_sqft_to_remove_this_year<0] = 0

        # Log pertinent information
        total_dus_to_remove_sum = total_dus_to_remove_this_year.sum()
        logger.log_status("\nTotal DUs demolished: %s" % total_dus_to_remove_sum) 
        total_non_residential_sqft_to_remove_sum = total_non_residential_sqft_to_remove_this_year.sum()
        logger.log_status("Total Non-Res sqft demolished: %s" % total_non_residential_sqft_to_remove_sum)

        #if total_dus_to_remove_sum==0 and total_non_residential_sqft_to_remove_sum==0:
        #    logger.log_status('No Redevelopment')
        #    return
        
        
        from numpy import array
        redev_ids_to_actually_do_something_with = []
        #if self.debuglevel > 0:        
        # set up a table to log into
        unit_log = PrettyTable()
        unit_log.set_field_names(["building_id","DUs demolished","NonRes Sqft demolished"])
        # log units demolished into table
        for indx in range(0,unique_redevelopment_building_ids.size):
            if total_dus_to_remove_this_year[indx] > 0 or total_non_residential_sqft_to_remove_this_year[indx] > 0:
                status_line = [unique_redevelopment_building_ids[indx],total_dus_to_remove_this_year[indx],total_non_residential_sqft_to_remove_this_year[indx]]
                unit_log.add_row(status_line)
                redev_ids_to_actually_do_something_with.append(unique_redevelopment_building_ids[indx])
        logger.log_status("\nUnits demolished by building_id:")
        logger.log_status(unit_log)

        ### Update building records
        # get attributes for updating
        residential_units_to_remove_from = self.buildings_dataset.get_attribute_by_id('residential_units',unique_redevelopment_building_ids)
        non_residential_sqft_to_remove_from = self.buildings_dataset.get_attribute_by_id('non_residential_sqft',unique_redevelopment_building_ids)

        new_residential_units = residential_units_to_remove_from - total_dus_to_remove_this_year
        new_non_residential_sqft = non_residential_sqft_to_remove_from - total_non_residential_sqft_to_remove_this_year
        
        redev_ids_to_actually_do_something_with_index = self.buildings_dataset.get_id_index(redev_ids_to_actually_do_something_with)
        unique_redevelopment_building_ids_index = self.buildings_dataset.get_id_index(unique_redevelopment_building_ids)
        self.buildings_dataset.set_values_of_one_attribute('residential_units', new_residential_units, unique_redevelopment_building_ids_index)
        self.buildings_dataset.set_values_of_one_attribute('non_residential_sqft', new_non_residential_sqft, unique_redevelopment_building_ids_index)

        #jesse testing
        print('\n####################################\n')
        print('total_dus_to_remove_this_year = %s' % total_dus_to_remove_this_year)
        print('total_non_residential_sqft_to_remove_this_year = %s' % total_non_residential_sqft_to_remove_this_year)
        print('redev_ids_to_actually_do_something_with = %s' % redev_ids_to_actually_do_something_with)
        print('redev_ids_to_actually_do_something_with_index = %s' % redev_ids_to_actually_do_something_with_index)
        print('unique_redevelopment_building_ids_index = %s' % unique_redevelopment_building_ids_index)
        print('\n####################################\n')

        ### Unplace building occupants
        # compute variables
        vacant_residential_units_with_negatives = \
            self.buildings_dataset.compute_variables("mag_zone.building.vacant_residential_units_with_negatives", dataset_pool=dataset_pool)
        vacant_non_home_based_job_spaces_with_negatives = \
            self.buildings_dataset.compute_variables('mag_zone.building.vacant_non_home_based_job_spaces_with_negatives', dataset_pool=dataset_pool)

#        # jesse testing
#        print '\n*****************************\n'
#        print vacant_residential_units_with_negatives[unique_redevelopment_building_ids_index]
#        print '\n-----------------------------\n'
#        print type(unique_redevelopment_building_ids_index)
#        print len(unique_redevelopment_building_ids_index)
#        print unique_redevelopment_building_ids_index
#        print '\n-----------------------------\n'
#        print type(vacant_residential_units_with_negatives)
#        print len(vacant_residential_units_with_negatives)
#        print vacant_residential_units_with_negatives
#        print '\n-----------------------------\n'
#        print type(vacant_non_home_based_job_spaces_with_negatives)
#        print len(vacant_non_home_based_job_spaces_with_negatives)
#        print vacant_non_home_based_job_spaces_with_negatives
#        print '\n*****************************\n'

        # Get jobs and households datasets
        self.jobs_dataset = dataset_pool.get_dataset('job')
        self.households_dataset = dataset_pool.get_dataset('household')

        # a list of tuples containing the computed space variables (including overfilled) and the dataset
        # of the occupants which may be overfilling the space
        #Jesse testing begin
        # old 2 lines 7/25:
        #check_for_overfilled = [(vacant_residential_units_with_negatives[unique_redevelopment_building_ids_index], self.households_dataset),
        #                        (vacant_non_home_based_job_spaces_with_negatives[unique_redevelopment_building_ids_index], self.jobs_dataset),]
        #new 2 lines 7/25:
        check_for_overfilled = [(vacant_residential_units_with_negatives[redev_ids_to_actually_do_something_with_index], self.households_dataset),
                                (vacant_non_home_based_job_spaces_with_negatives[redev_ids_to_actually_do_something_with_index], self.jobs_dataset),]
        #Jesse testing end
        #OLD CODE:
#        check_for_overfilled = [(vacant_residential_units_with_negatives[unique_redevelopment_building_ids_index], self.households_dataset),
#                                (vacant_non_home_based_job_spaces_with_negatives[unique_redevelopment_building_ids_index], self.jobs_dataset),]

        #print '\n(((((((((((((((((((((((((((((((((((((((((((\n'
        #print vacant_residential_units_with_negatives[unique_redevelopment_building_ids_index]
        #print vacant_non_home_based_job_spaces_with_negatives[unique_redevelopment_building_ids_index]
        #print '\n(((((((((((((((((((((((((((((((((((((((((((\n'
        
        
        # check for negative spaces (indicating overfilled buildings), if negatives are found, then 
        # randomly unplace agents until the space is no longer overfilled
        counter = 0
        for spaces_with_negatives, dataset in check_for_overfilled:
            if True in (spaces_with_negatives<0):
                index_overfilled_spaces = where(spaces_with_negatives<0)[0]
                # 7/25, NEXT LINE REPLACED 'unique_redevelopment_building_ids_index' WITH redev_ids_to_actually_do_something_with_index
                occupants_log = self.sample_and_unplace_agents(spaces_with_negatives, dataset, redev_ids_to_actually_do_something_with_index, index_overfilled_spaces)
                if self.debuglevel > 0:
                    if counter == 0:
                        logger.log_status("\nBuilding occupants unplaced by building_id for residential buildings:")
                        logger.log_status(occupants_log)
                        occupants_log = ''
                    elif counter:
                        if occupants_log == '':
                            pass
                        else:
                            logger.log_status("\nBuilding occupants unplaced by building_id for non-residential buildings:")
                            logger.log_status(occupants_log)
            counter += 1
                    

    def sample_and_unplace_agents(self, spaces_with_negatives, dataset, unique_redevelopment_building_ids_index, index_overfilled_spaces):
        """
        Using overfilled spaces, agents, and buildings, randomly sample and unplace agents until the spaces are 
        no longer overfilled.
            - spaces_with_negatives is an array of vacant residential or job spaces that includes negative values (overfilled)
            - dataset is the dataset of agents overfilling the spaces specified in spaces_with_negatives
        """
        
        # jesse testing
        print('\n[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[\n')
        print(spaces_with_negatives)
        print(unique_redevelopment_building_ids_index)
        print(index_overfilled_spaces)
        
        # set up table for logging unplaced building occupants
        occupants_log = PrettyTable()
        occupants_log.set_field_names(["building_id","HH unplaced","Jobs unplaced","HB Jobs unplaced"])

        #index_overfilled_spaces = where(spaces_with_negatives<0)[0]
        #print '\n+++++++++++++++++++++++++++\n'
        #print '\nindex_overfilled_spaces = %s' % index_overfilled_spaces
        #print type(index_overfilled_spaces)
        number_of_overfilled_spaces = abs(spaces_with_negatives[index_overfilled_spaces].astype('int'))
        #print '\nnumber_of_overfilled_spaces = %s' % number_of_overfilled_spaces
        #print type(number_of_overfilled_spaces)
        overfilled_spaces_building_ids = self.buildings_dataset.get_id_attribute()[unique_redevelopment_building_ids_index]
        overfilled_spaces_building_ids = overfilled_spaces_building_ids[index_overfilled_spaces]
        print('\n0000000000000000000000000000000000')
        print('\noverfilled_spaces_building_ids = %s' % overfilled_spaces_building_ids)
        print(type(overfilled_spaces_building_ids))
        look_for_home_based_jobs = False
        dataset_name = dataset.get_dataset_name()
        #print '\ndataset_name = %s' % dataset_name
        if 'household' in dataset_name:
            look_for_home_based_jobs = True
        for building_id, number_of_agents_to_unplace in zip(overfilled_spaces_building_ids, number_of_overfilled_spaces):
            #print '\nbuilding_id = %s' % building_id
            #print '\nnumber_of_agents_to_unplace = %s\n' % number_of_agents_to_unplace
            occupants_log_line = []
            occupants_log_line.append(building_id)
            index_of_agents_to_sample_from = dataset.get_filtered_index('%s.building_id==%s' % (dataset_name,building_id))
            #print '\nsize of index_of_agents_to_sample_from = %s\n' % len(index_of_agents_to_sample_from)
            sample_of_agents_to_unplace = sample_noreplace(index_of_agents_to_sample_from, number_of_agents_to_unplace)
            dataset.set_values_of_one_attribute('building_id', array([-1]), sample_of_agents_to_unplace)
            if look_for_home_based_jobs:
                occupants_log_line.append(number_of_agents_to_unplace)
                occupants_log_line.append(0)
                number_of_home_based_jobs_to_unplace = self.unplace_home_based_jobs(building_id)
                occupants_log_line.append(number_of_home_based_jobs_to_unplace)
            else:
                occupants_log_line.append(0)
                occupants_log_line.append(number_of_agents_to_unplace)
                occupants_log_line.append(0)
            occupants_log.add_row(occupants_log_line)
        #print '\n+++++++++++++++++++++++++++\n'
        return occupants_log

    def unplace_home_based_jobs(self, building_id):
        """
        If households are being unplaced, check the building_ids that those households occupied for any home_based_jobs
        that need to be unplaced as well.
        """
        # get the index of the building to check
        building_index = self.buildings_dataset.get_id_index(building_id)
        # compute some necessary variables
        number_of_home_based_jobs = self.buildings_dataset.compute_variables("urbansim_zone.building.number_of_home_based_jobs", dataset_pool=self.dataset_pool).astype('int')
        number_of_home_based_job_spaces = self.buildings_dataset.compute_variables("urbansim_zone.building.total_home_based_job_spaces", dataset_pool=self.dataset_pool).astype('int')
        number_of_home_based_jobs_in_building = number_of_home_based_jobs[building_index]
        number_of_home_based_job_spaces_in_building = number_of_home_based_job_spaces[building_index]
        number_of_home_based_jobs_to_unplace = number_of_home_based_jobs_in_building - number_of_home_based_job_spaces_in_building
        if number_of_home_based_jobs_to_unplace < 1:
            return 0
        # unplace jobs
        # get jobs to sample from
        index_of_jobs_to_sample_from = self.jobs_dataset.get_filtered_index('job.building_id==%s' % building_id)
        sample_of_jobs_to_unplace = sample_noreplace(index_of_jobs_to_sample_from, number_of_home_based_jobs_to_unplace)
        self.jobs_dataset.set_values_of_one_attribute('building_id', array([-1]), sample_of_jobs_to_unplace)
        return number_of_home_based_jobs_to_unplace


from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import array, arange, int, ones, zeros, concatenate, append

class PlannedRedevelopmentResidualModelTest(opus_unittest.OpusTestCase):

    def test_case01(self):
        # The buildings_data in this example represents the case when the developer
        # model develops 4000 non_residential_sqft, which will take the place of 
        # 40 residential_units
        buildings_data = {
                                          'zone_id' : array([45,45]),
                                      'building_id' : array([57,58]),
                                 'building_type_id' : array([1,3]),
                                'residential_units' : array([100,0]),
                             'non_residential_sqft' : array([0,4000]),
                       'residential_units_capacity' : array([0,0]),
                    'non_residential_sqft_capacity' : array([0,10000]),
                                        'land_area' : array([871200,871200]),
                      'base_year_residential_units' : array([100,0]),
                   'base_year_non_residential_sqft' : array([0,0]),
                        'redevelopment_building_id' : array([-1,57]),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56
                           }
        jobs_data = {
                                            'job_id':arange(10)+1,
                                       'building_id':ones(10).astype('int'),
                                       'home_based_status':zeros(10).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==60, True)
        # check that there are 40 unplaced households
        households_dataset = self.dataset_pool.get_dataset('household')
        total_unplaced_households = where(households_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_households==40,True)

    def test_case01a(self):
        # The buildings_data in this example represents the case when the developer
        # model develops 4000 non_residential_sqft, which will take the place of 
        # 40 residential_units.  This test also adds an extra, overfilled building.
        buildings_data = {
                                          'zone_id' : append(array([45,45]),array([46,46,46,46,46,46,46,46,46,46,46,46,46,46,46])),
                                      'building_id' : append(array([57,58]),arange(59,74)),
                                 'building_type_id' : append(array([1,3]),array([5 for i in range(15)])),
                                'residential_units' : append(array([100,0]),zeros(15)),
                             'non_residential_sqft' : append(array([0,4000]),array([100 for i in range(15)])),
                       'residential_units_capacity' : append(array([0,0]),zeros(15)),
                    'non_residential_sqft_capacity' : append(array([0,10000]),array([100 for i in range(15)])),
                                        'land_area' : append(array([871200,871200]),array([871200 for i in range(15)])),
                      'base_year_residential_units' : append(array([100,0]),zeros(15)),
                   'base_year_non_residential_sqft' : append(array([0,0]),array([100 for i in range(15)])),
                        'redevelopment_building_id' : append(array([-1,57]),array([-1 for i in range(15)])),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56
                           }
        jobs_data = {
                                            'job_id':arange(40)+1,
                                       'building_id':append(append(ones(10).astype('int'),arange(59,74)),arange(59,74)),
                                       'home_based_status':zeros(40).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45,46]),
                                  'building_type_id':array([1,3,5]),
                             'building_sqft_per_job':array([1000,1000,100]),
                                      }

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==60, True)
        # check that there are 40 unplaced households
        households_dataset = self.dataset_pool.get_dataset('household')
        total_unplaced_households = where(households_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_households==40,True)

    def test_case02(self):
        # The buildings data in this example represent the case when the developer
        # model develops 8000 non_residential_sqft, which will take the place of
        # 23 residential_units
        buildings_data = {
                                          'zone_id' : array([45,45,45,45,45]),
                                      'building_id' : array([57,58,59,60,61]),
                                 'building_type_id' : array([1,4,5,1,3]),
                                'residential_units' : array([100,0,0,50,0]),
                             'non_residential_sqft' : array([0,2000,6000,0,32000]),
                       'residential_units_capacity' : array([0,0,0,57,0]),
                    'non_residential_sqft_capacity' : array([0,10000,25000,0,52000]),
                                        'land_area' : array([435600,130680,304920,653400,304920]),
                      'base_year_residential_units' : array([100,0,0,50,0]),
                   'base_year_non_residential_sqft' : array([0,0,0,0,32000]),
                        'redevelopment_building_id' : array([-1,57,57,-1,-1]),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56
                           }
        jobs_data = {
                                            'job_id':arange(10)+1,
                                       'building_id':ones(10).astype('int'),
                                       'home_based_status':zeros(10).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==77, True)
        # check that there are 23 unplaced households
        households_dataset = self.dataset_pool.get_dataset('household')
        total_unplaced_households = where(households_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_households==23,True)

    def test_case03(self):
        # The buildings data in this example combine examples 1 and 2
        buildings_data = {
                                          'zone_id' : array([45,45,45,45,45,45,45]),
                                      'building_id' : array([57,58,59,60,61,62,63]),
                                 'building_type_id' : array([1,3,1,4,5,1,3]),
                                'residential_units' : array([100,0,100,0,0,50,0]),
                             'non_residential_sqft' : array([0,4000,0,2000,6000,0,32000]),
                       'residential_units_capacity' : array([0,0,0,0,0,57,0]),
                    'non_residential_sqft_capacity' : array([0,10000,0,10000,25000,0,52000]),
                                        'land_area' : array([871200,871200,435600,130680,304920,653400,304920]),
                      'base_year_residential_units' : array([100,0,100,0,0,50,0]),
                   'base_year_non_residential_sqft' : array([0,0,0,0,0,0,32000]),
                        'redevelopment_building_id' : array([-1,57,-1,59,59,-1,-1]),
                          }
        households_data = {
                                      'household_id':arange(200)+1,
                                       'building_id':concatenate([ones(100).astype('int')+56,ones(100).astype('int')+58])
                           }
        jobs_data = {
                                            'job_id':arange(10)+1,
                                       'building_id':ones(10).astype('int'),
                                       'home_based_status':zeros(10).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        #jesse testing
        print('\n\nBEGIN TEST 03\n\n')
        #end jesse testing
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==60, True)
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[2]==77, True)
        # check that there are 63 unplaced households
        households_dataset = self.dataset_pool.get_dataset('household')
        total_unplaced_households = where(households_dataset.get_attribute('building_id')<0)[0].size
        #jesse testing
        print('\n-----------------\ntotal_unplaced_households: %s' % total_unplaced_households)
        print('\n\nEND TEST 03\n\n')
        #end jesse testing
        self.assertEqual(total_unplaced_households==63,True)

    def test_case04(self):
        # The buildings_data in this example reverses case #1, the developer
        # model develops 40 residential units, which will take the place of 
        # 4000 non-residential sqft
        buildings_data = {
                                          'zone_id' : array([45,45]),
                                      'building_id' : array([57,58]),
                                 'building_type_id' : array([3,1]),
                                'residential_units' : array([0,40]),
                             'non_residential_sqft' : array([10000,0]),
                       'residential_units_capacity' : array([0,100]),
                    'non_residential_sqft_capacity' : array([10000,0]),
                                        'land_area' : array([871200,871200]),
                      'base_year_residential_units' : array([0,0]),
                   'base_year_non_residential_sqft' : array([10000,0]),
                        'redevelopment_building_id' : array([-1,57]),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')
                           }
        jobs_data = {
                                            'job_id':arange(10)+1,
                                       'building_id':ones(10).astype('int')+56,
                                       'home_based_status':zeros(10).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('non_residential_sqft')[0]==6000, True)
        # check that unplaced jobs == 4
        jobs_dataset = self.dataset_pool.get_dataset('job')
        total_unplaced_jobs = where(jobs_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_jobs==4, True)
        
    def test_case05(self):
        # The buildings data in this example reverses case #2, the developer
        # model develops a total of 80 residential units, which will take the place of
        # 18240 non-residential sqft
        buildings_data = {
                                          'zone_id' : array([45,45,45,45,45]),
                                      'building_id' : array([57,58,59,60,61]),
                                 'building_type_id' : array([4,1,2,1,3]),
                                'residential_units' : array([0,20,60,50,0]),
                             'non_residential_sqft' : array([80000,0,0,0,32000]),
                       'residential_units_capacity' : array([0,100,250,57,0]),
                    'non_residential_sqft_capacity' : array([0,0,0,0,52000]),
                                        'land_area' : array([435600,130680,304920,653400,304920]),
                      'base_year_residential_units' : array([0,0,0,50,0]),
                   'base_year_non_residential_sqft' : array([80000,0,0,0,32000]),
                        'redevelopment_building_id' : array([-1,57,57,-1,-1]),
                          }
        households_data = {
                                      'household_id':arange(10)+1,
                                       'building_id':ones(10).astype('int')
                           }
        jobs_data = {
                                            'job_id':arange(80)+1,
                                       'building_id':ones(80).astype('int')+56,
                                       'home_based_status':zeros(80).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('non_residential_sqft')[0]==61760, True)
        # check that unplaced jobs == 18
        jobs_dataset = self.dataset_pool.get_dataset('job')
        total_unplaced_jobs = where(jobs_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_jobs==18, True)
             
    def test_case06(self):
        # The buildings_data in this example combines cases 4&5, the developer
        # model develops 40 residential units, which will take the place of 
        # 4000 non-residential units and develops a total of 80 residential units, which will take the place of
        # 18240 non-residential sqft
        buildings_data = {
                                          'zone_id' : array([45,45,45,45,45,45,45]),
                                      'building_id' : array([57,58,59,60,61,62,63]),
                                 'building_type_id' : array([3,1,4,1,2,1,3]),
                                'residential_units' : array([0,40,0,20,60,50,0]),
                             'non_residential_sqft' : array([10000,0,80000,0,0,0,32000]),
                       'residential_units_capacity' : array([0,100,0,100,250,57,0]),
                    'non_residential_sqft_capacity' : array([10000,0,0,0,0,0,52000]),
                                        'land_area' : array([871200,871200,435600,130680,304920,653400,304920]),
                      'base_year_residential_units' : array([0,0,0,0,0,50,0]),
                   'base_year_non_residential_sqft' : array([10000,0,80000,0,0,0,0]),
                        'redevelopment_building_id' : array([-1,57,-1,59,59,-1,-1]),
                          }
        households_data = {
                                      'household_id':arange(10)+1,
                                       'building_id':ones(10).astype('int')
                           }
        jobs_data = {
                                            'job_id':arange(90)+1,
                                       'building_id':concatenate([ones(80).astype('int')+56,ones(10).astype('int')+58]),
                                       'home_based_status':zeros(90).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('non_residential_sqft')[0]==6000, True)
        self.assertEqual(buildings_dataset.get_attribute('non_residential_sqft')[2]==61760, True)
        # check that unplaced jobs == 22
        jobs_dataset = self.dataset_pool.get_dataset('job')
        total_unplaced_jobs = where(jobs_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_jobs==74, True)

    def test_case07(self):
        # The buildings_data in this example represents a combination of test cases
        # 1 and 4 to test the case where both DUs and non-res sqft are being re-developed 
        buildings_data = {
                                          'zone_id' : array([45,45,45,45]),
                                      'building_id' : array([57,58,59,60]),
                                 'building_type_id' : array([1,3,3,1]),
                                'residential_units' : array([100,0,0,40]),
                             'non_residential_sqft' : array([0,4000,10000,0]),
                       'residential_units_capacity' : array([0,0,0,100]),
                    'non_residential_sqft_capacity' : array([0,10000,10000,0]),
                                        'land_area' : array([871200,871200,871200,871200]),
                      'base_year_residential_units' : array([100,0,0,0]),
                   'base_year_non_residential_sqft' : array([0,0,10000,0]),
                        'redevelopment_building_id' : array([-1,57,-1,59]),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56
                           }
        jobs_data = {
                                            'job_id':arange(10)+1,
                                       'building_id':ones(10).astype('int')+58,
                                       'home_based_status':zeros(10).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that there are appropriate numbers of dus and sqft
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==60, True)
        self.assertEqual(buildings_dataset.get_attribute('non_residential_sqft')[2]==6000, True)
        # check that there are 6 placed jobs
        jobs_dataset = self.dataset_pool.get_dataset('job')
        unplaced_jobs = where(jobs_dataset.get_attribute('building_id')<1)[0].size
        print('\nunplaced_jobs = %s\n' % unplaced_jobs)
        self.assertEqual(unplaced_jobs==4, True)
        # check that there are 40 unplaced households
        households_dataset = self.dataset_pool.get_dataset('household')
        total_unplaced_households = where(households_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_households==40, True)
        
    def test_case08(self):
        # The buildings_data in this example represents the case when the developer
        # model develops 4000 non_residential_sqft, which will take the place of 
        # 40 residential_units, this will also displace 40 home_based_jobs as well
        buildings_data = {
                                          'zone_id' : array([45,45]),
                                      'building_id' : array([57,58]),
                                 'building_type_id' : array([1,3]),
                                'residential_units' : array([100,0]),
                             'non_residential_sqft' : array([0,4000]),
                       'residential_units_capacity' : array([0,0]),
                    'non_residential_sqft_capacity' : array([0,10000]),
                                        'land_area' : array([871200,871200]),
                      'base_year_residential_units' : array([100,0]),
                   'base_year_non_residential_sqft' : array([0,0]),
                        'redevelopment_building_id' : array([-1,57]),
                          }
        households_data = {
                                      'household_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56
                           }
        jobs_data = {
                                            'job_id':arange(100)+1,
                                       'building_id':ones(100).astype('int')+56,
                                       'home_based_status':ones(100).astype('int'),
                    }
        building_sqft_per_job_data = {
                                           'zone_id':array([45,45]),
                                  'building_type_id':array([1,3]),
                             'building_sqft_per_job':array([1000,1000]),
                                      }

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='buildings', table_data=buildings_data)
        storage.write_table(table_name='households', table_data=households_data)
        storage.write_table(table_name='jobs', table_data=jobs_data)
        storage.write_table(table_name='building_sqft_per_job', table_data=building_sqft_per_job_data)
        self.dataset_pool = DatasetPool(storage = storage, package_order = ['mag_zone','urbansim_zone','urbansim','opus_core'])
        model = PlannedRedevelopmentResidualModel(debuglevel=0)
        model.run(dataset_pool=self.dataset_pool)
        # check that total residential units == 60
        buildings_dataset = self.dataset_pool.get_dataset('building')
        self.assertEqual(buildings_dataset.get_attribute('residential_units')[0]==60, True)
        # check that unplaced jobs == 40
        jobs_dataset = self.dataset_pool.get_dataset('job')
        total_unplaced_jobs = where(jobs_dataset.get_attribute('building_id')<0)[0].size
        self.assertEqual(total_unplaced_jobs==40, True)
        # check that total placed households == 60
        households_dataset = self.dataset_pool.get_dataset('household')
        total_placed_households = where(households_dataset.get_attribute('building_id')>0)[0].size
        self.assertEqual(total_placed_households==60, True)
        
if __name__=="__main__":
    opus_unittest.main()
