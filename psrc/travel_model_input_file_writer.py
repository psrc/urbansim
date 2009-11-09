# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import time
from opus_core.logger import logger
from numpy import logical_or, logical_and, logical_not, array, where, zeros, median
from opus_core.datasets.dataset import DatasetSubset

class TravelModelInputFileWriter(object):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. """

    def run(self, current_year_emme2_dir, current_year, dataset_pool, config=None):
        """Writes to the an emme2 input file in the [current_year_emme2_dir]/tripgen/inputtg/tazdata.ma2.
        """
        
        missing_dataset = ''
        try:
            missing_dataset = 'constant_taz_column'
            taz_col_set = dataset_pool.get_dataset("constant_taz_column")
            taz_col_set.load_dataset()
            missing_dataset = 'zone'
            zone_set = dataset_pool.get_dataset("zone")
            zone_set.load_dataset()
            missing_dataset = 'household'
            household_set = dataset_pool.get_dataset("household")
        except:
            raise Exception("Dataset %s is missing from dataset_pool" % missing_dataset)
        
        """specify travel input file name: [current_year_emme2_dir]/tripgen/inputtg/tazdata.ma2 """
        full_path = os.path.join(current_year_emme2_dir, 'tripgen', 'inputtg')
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        tm_input_file = os.path.join(full_path, 'tazdata.ma2')
        
        tm_year = self._decade_floor(current_year)
        
        logger.log_status("calculating entries for emme2 input file")
        taz_col_set.compute_variables("zone_id=constant_taz_column.taz")
        current_taz_col = DatasetSubset(taz_col_set, index=where(taz_col_set.get_attribute("year")==tm_year)[0])
        
        current_taz_col._id_names = ['taz']
        current_taz_col._create_id_mapping()
        zone_set.join(current_taz_col, "pctmf", join_attribute='zone_id')
        zone_set.join(current_taz_col, "gqi", join_attribute='zone_id')
        zone_set.join(current_taz_col, "gqn", join_attribute='zone_id')
        zone_set.join(current_taz_col, "fteuniv", join_attribute='zone_id')
        zone_set.join(current_taz_col, "den", new_name='density', join_attribute='zone_id')

        value_122 = zeros(zone_set.size())
        index_122 = zone_set.try_get_id_index(array([58,59,60,71,72,73,84,85,86,150,251,266,489,578,687,688,797,868]))
        value_122[index_122[index_122 != -1]] = 1
        zone_set.add_attribute(data=value_122, name="v122")
        
        value_123 = zeros(zone_set.size())
        index_123 = zone_set.try_get_id_index(array([531,646,847,850,888,894,899,910]))
        value_123[index_123[index_123 != -1]] = 1
        zone_set.add_attribute(data=value_123, name="v123")
        
        value_124 = logical_not(value_122 + value_123)
        zone_set.add_attribute(data=value_124, name="v124")
                
        """specify which variables are passing from urbansim to travel model; the order matters"""
        variables_list = self.get_variables_list(dataset_pool)
        
        zone_set.compute_variables(variables_list, dataset_pool=dataset_pool )

        return self._write_to_file(zone_set, variables_list, tm_input_file)

    def get_variables_list(self, dataset_pool):
        first_quarter, median_income, third_quarter = self._get_income_group_quartiles(dataset_pool)
        return [
            "pctmf",  #101
            "hhs_of_first_quarter = zone.aggregate(household.income < %s)" % first_quarter, #102
            "hhs_of_second_quarter = zone.aggregate(numpy.logical_and(household.income >= %s, household.income < %s))" % (first_quarter, median_income), #103
            "hhs_of_third_quarter = zone.aggregate(numpy.logical_and(household.income >= %s, household.income < %s))" % (median_income, third_quarter),  #104
            "hhs_of_fourth_quarter = zone.aggregate(household.income >= %s)" % third_quarter, #105
            'gqi', #106
            'gqn', #107
            '-1 + 0 * zone.zone_id',  #108 unsed, set to -1
            "density_1_retail_jobs = (zone.density==1).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_retail)", #109
            "density_2_retail_jobs = (zone.density==2).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_retail)", #110
            "density_3_retail_jobs = (zone.density==3).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_retail)", #111
            "density_1_fires_jobs = (zone.density==1).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_fires)",   #112
            "density_2_fires_jobs = (zone.density==2).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_fires)",   #113
            "density_3_fires_jobs = (zone.density==3).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_fires)",   #114
            "density_1_gov_jobs = (zone.density==1).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_gov)",       #115
            "density_2_gov_jobs = (zone.density==2).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_gov)",       #116
            "density_3_gov_jobs = (zone.density==3).astype(float32) * zone.aggregate(urbansim.job.is_in_employment_sector_group_gov)",       #117 
            "edu_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_edu)",     #118
            "wtcu_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_wtcu)",   #119
            "manu_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_manu)",   #120
            "fteuniv",                   #121
            'zone.gqn * zone.v122',      #122
            'zone.gqn * zone.v123',      #123
            'zone.gqn * zone.v124'       #124
            ]
        
    def _get_income_group_quartiles(self, dataset_pool):
        household_set = dataset_pool.get_dataset("household")
        # setup for calculating quartile information
        hh_income = household_set.get_attribute("income")
        median_income = median(hh_income)
        first_quarter = median(hh_income[where(hh_income<median_income)])
        third_quarter = median(hh_income[where(hh_income>median_income)])
        return (first_quarter, median_income, third_quarter)
    
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        logger.start_block("Writing to emme2 input file: " + tm_input_file)
        try:
            newfile = open(tm_input_file, 'w')
            """write travel model input file into a particular file format emme2 can read"""
            try:
                newfile.write(r"""c  from
c  prepared: %s
t matrices
m matrix="hhemp"
""" % time.strftime("%c", time.localtime(time.time())))
                
                line_template = "%4d    %3d: %8.2f \n"
                for taz_id in zone_set.get_id_attribute():
                    for i in range(101, 125):
                        newfile.write(line_template % (taz_id, i, self._get_value_for_zone(taz_id, zone_set, variables_list[i-101])))
            finally:
                newfile.close()
        finally:
            logger.end_block()
        return tm_input_file

    def _get_value_for_zone(self, zone_id, zone_set, variable_name):
        return zone_set.get_attribute_by_id(variable_name, zone_id)

    def _decade_floor(self, year):
        return int(round(year - 5, -1))
