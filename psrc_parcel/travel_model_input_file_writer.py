# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
import time
from numpy import where, logical_and
from opus_core.logger import logger
from psrc.travel_model_input_file_writer import TravelModelInputFileWriter as HHJobsTravelModelInputFileWriter

class TravelModelInputFileWriter(HHJobsTravelModelInputFileWriter):
    """Write urbansim simulation information into a (file) format that the emme2 travel model understands. 
        It creates tazdata.MA2 with informations about households and jobs, and tazdata.mf91, tazdata.mf92, tazdata.mf93, tazdata.mf94
        with information about people's workplaces.
    """

    def run(self, current_year_emme2_dir, current_year, dataset_pool, config=None):
        """Writes emme2 input files into the [current_year_emme2_dir]/tripgen/inputtg/
        """
        tm_input_file_1 = HHJobsTravelModelInputFileWriter.run(self, current_year_emme2_dir, current_year, dataset_pool, config) # writes TAZDATA.MA2
        
        missing_dataset = ''
        try:
            missing_dataset = 'person'
            person_set = dataset_pool.get_dataset("person")
        except:
            raise "Dataset %s is missing from dataset_pool" % missing_dataset
        
        """specify travel input file name: [current_year_emme2_dir]/tripgen/inputtg/tazdata.ma2 """
        full_path = os.path.join(current_year_emme2_dir, 'tripgen', 'inputtg')
        tm_input_files = [os.path.join(full_path, 'tazdata.mf91'), os.path.join(full_path, 'tazdata.mf92'),
                         os.path.join(full_path, 'tazdata.mf93'), os.path.join(full_path, 'tazdata.mf94')]
                
        first_quarter, median_income, third_quarter = self._get_income_group_quartiles(dataset_pool)
        logger.log_status("calculating entries for emme2 *.mf9x input files")

        household_variables_to_compute = ["is_income_group_1 = household.income < %s" % first_quarter,
                                "is_income_group_2 = numpy.logical_and(household.income >= %s, household.income < %s)" % (first_quarter, median_income),
                                "is_income_group_3 = numpy.logical_and(household.income >= %s, household.income < %s)" % (median_income, third_quarter),
                                "is_income_group_4 = household.income >= %s" % third_quarter]
        
        dataset_pool.get_dataset("household").compute_variables(household_variables_to_compute, dataset_pool=dataset_pool)
        person_variables_to_compute = [
                                "income_group_1 = person.disaggregate(household.is_income_group_1)",
                                "income_group_2 = person.disaggregate(household.is_income_group_2)",
                                "income_group_3 = person.disaggregate(household.is_income_group_3)",
                                "income_group_4 = person.disaggregate(household.is_income_group_4)",
                                "urbansim_parcel.person.zone_id",
                                "urbansim_parcel.person.is_placed_non_home_based_worker_with_job",
                                "job_zone_id = person.disaggregate(urbansim_parcel.job.zone_id)"
                                ]
        
        person_set.compute_variables(person_variables_to_compute, dataset_pool=dataset_pool)

        return [tm_input_file_1] + self._write_workplaces_to_files(person_set, tm_input_files)


        
    def _write_workplaces_to_files(self, person_set, tm_input_files):
        home_zones = person_set.get_attribute("zone_id")
        job_zones = person_set.get_attribute("job_zone_id")
        igroup = 0
        for tm_file in tm_input_files:
            logger.start_block("Writing to emme2 input file: " + tm_input_files[igroup])
            try:
                newfile = open(tm_input_files[igroup], 'w')
                try:
                    newfile.write(r"""c  prepared: %s
t matrices
m matrix=mf9%s default=incr
""" % (time.strftime("%c", time.localtime(time.time())), igroup+1))
                    line_template = " %3d    %3d    1 \n"
                    person_idx = where(logical_and(person_set.get_attribute("is_placed_non_home_based_worker_with_job"), 
                                                   person_set.get_attribute("income_group_%s" % (igroup+1))))[0]
                    for i in person_idx:
                        newfile.write(line_template % (home_zones[i], job_zones[i]))
                finally:
                    newfile.close()
            finally:
                logger.end_block()
            igroup+=1
        return tm_input_files

