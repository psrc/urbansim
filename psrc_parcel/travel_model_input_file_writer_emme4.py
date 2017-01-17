# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import time
from numpy import where, logical_and, abs, sort
from opus_core.logger import logger
from psrc_parcel.travel_model_input_file_writer import TravelModelInputFileWriter as ParentTravelModelInputFileWriter
from opus_core.datasets.dataset import DatasetSubset

class TravelModelInputFileWriterEmme4(ParentTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme4 travel model understands. 
    """
    emme_version = 4
    def run(self, current_year_emme2_dir, current_year, dataset_pool, config):
        """Writes emme4 input files into the appropriate place at [current_year_emme2_dir]
        """
        input_dir = config['travel_model_configuration'].get('emme_input_directory', 
                                os.path.join(current_year_emme2_dir, "landuse"))
        tm_input_file_1 = self._write_input_file_1(current_year_emme2_dir, input_dir, current_year, dataset_pool, config) # writes tazdata.in
        return [tm_input_file_1]

    def _write_input_file_1(self, current_year_emme2_dir, input_dir, current_year, dataset_pool, config=None):
        missing_dataset = ''
        try:
            missing_dataset = 'group_quarter'
            taz_col_set = dataset_pool.get_dataset("group_quarter")
            taz_col_set.load_dataset()
            missing_dataset = 'zone'
            zone_set = dataset_pool.get_dataset("zone")
            zone_set.load_dataset()
            missing_dataset = 'household'
            household_set = dataset_pool.get_dataset("household")
        except:
            raise Exception("Dataset %s is missing from dataset_pool" % missing_dataset)
        
        """specify travel input file name """
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        tm_input_file = os.path.join(input_dir, 'tazdata.in')
        
        tm_year = self._get_tm_year(current_year, taz_col_set)
        
        logger.log_status("calculating entries for emme%s input file" % self.emme_version)
        taz_col_set.compute_variables("zone_id=group_quarter.taz")
        current_taz_col = DatasetSubset(taz_col_set, index=where(taz_col_set.get_attribute("year")==tm_year)[0])
        
        current_taz_col._id_names = ['taz']
        current_taz_col._create_id_mapping()
        zone_set.join(current_taz_col, "gqdorm", join_attribute='zone_id')
        zone_set.join(current_taz_col, "gqmil", join_attribute='zone_id')
        zone_set.join(current_taz_col, "gqoth", join_attribute='zone_id')
        zone_set.join(current_taz_col, "fteuniv", join_attribute='zone_id')
              
        """specify which variables are passing from urbansim to travel model; the order matters"""
        variables_list = self.get_variables_list(dataset_pool, tm_year)
        
        zone_set.compute_variables(variables_list, dataset_pool=dataset_pool )

        return self._write_to_file(zone_set, variables_list, tm_input_file, tm_year)

    def get_variables_list(self, dataset_pool, year):
        first_quarter, median_income, third_quarter = self._get_income_group_quartiles(dataset_pool, year)
        return [
            "0 * zone.zone_id",  #101
            "hhs_of_first_quarter = zone.aggregate(household.income < %s)" % first_quarter, #102
            "hhs_of_second_quarter = zone.aggregate(numpy.logical_and(household.income >= %s, household.income < %s))" % (first_quarter, median_income), #103
            "hhs_of_third_quarter = zone.aggregate(numpy.logical_and(household.income >= %s, household.income < %s))" % (median_income, third_quarter),  #104
            "hhs_of_fourth_quarter = zone.aggregate(household.income >= %s)" % third_quarter, #105
            '0 * zone.zone_id', #106
            '0 * zone.zone_id', #107
            '0 * zone.zone_id',  #108 
            "retail_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_retail)", #109
            "0 * zone.zone_id", #110
            "0 * zone.zone_id", #111
            "fires_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_fires)",   #112
            "0 * zone.zone_id",   #113
            "0 * zone.zone_id",   #114
            "gov_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_gov)",       #115
            "0 * zone.zone_id",       #116
            "0 * zone.zone_id",       #117 
            "edu_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_edu)",     #118
            "0 * zone.zone_id",   #119
            "manu_jobs = zone.aggregate(urbansim.job.is_in_employment_sector_group_manu + urbansim.job.is_in_employment_sector_group_wtcu)",   #120
            "fteuniv",                   #121
            'zone.gqdorm',      #122
            'zone.gqmil',      #123
            'zone.gqoth'       #124
            ]
        
    def _get_income_group_quartiles(self, dataset_pool, year):
        #return (34000, 68000, 102000)
        #return (25000, 51000, 78000)
        #return (30000, 59000, 90000) # removes real income growth
        default_groups = (37000, 74000, 111000)
        income_groups = {
            2014: default_groups,
            2020: default_groups
        }
        return income_groups.get(year, default_groups)
    
    def _get_tm_year(self, year, gq):
        """Get the closest year to the current year in the group_quarters table."""
        years = gq['year']
        dif = abs(years - year)
        return years[where(dif == dif.min())[0]][0] 
    
    def _write_to_file(self, zone_set, variables_list, tm_input_file, tm_year):
        logger.start_block("Writing to emme%s input file: %s" % (self.emme_version, tm_input_file))
        try:
            newfile = open(tm_input_file, 'w')
            """write travel model input file into a particular file format emme2 can read"""
            try:
                newfile.write(r"""c prepared: %s
c %s
t matrices
m matrix="hhemp"
""" % (time.strftime("%c", time.localtime(time.time())), tm_year))
                line_template = "%s %s: %i \n"
                for taz_id in sort(zone_set.get_id_attribute()):
                    for i in range(101, 125):
                        newfile.write(line_template % (taz_id, i, self._get_value_for_zone(taz_id, zone_set, variables_list[i-101])))
            finally:
                newfile.close()
        finally:
            logger.end_block()
        return tm_input_file