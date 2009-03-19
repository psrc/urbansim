# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from scipy import ndimage
from numpy import ones, where, logical_and, arange, zeros
from travel_model_input_file_writer import TravelModelInputFileWriter
from opus_core.logger import logger
import os
import time

class TravelModelInputFileWriterLandUseDistr(TravelModelInputFileWriter):
    
    file_dir = "/Users/hana/tmp/lu_distr"
    
    def _write_to_file(self, zone_set, variables_list, tm_input_file):
        self.generate_travel_model_input(zone_set)
        self. _write_to_file_local(zone_set, self.full_variable_list, tm_input_file)
        
    def _write_to_file_local(self, zone_set, variables_list, tm_input_file):
        logger.start_block("Writing to emme2 input file: " + tm_input_file)
        newfile = open(tm_input_file, 'w')
        """write travel model input file into a particular file format emme2 can read"""
        newfile.write(r"""c  from
c  prepared: %s
t matrices
m matrix="hhemp"
""" % time.strftime("%c", time.localtime(time.time())))
        
        line_template = "%4d    %3d: %8.2f \n"
        for taz_id in zone_set.get_id_attribute():
            ####
            if taz_id in [189, 97, 119, 107, 344, 181]:
                tmpvalues = zeros(16)
                i=0
                for ivar in range(1,5)+range(8,20):
                    tmpvalues[i] = self._get_value_for_zone(taz_id, zone_set, variables_list[ivar])
                    i += 1
                tmp_file_name = os.path.join(self.file_dir, 'in_%s_propfac' % taz_id)
                if not os.path.exists(tmp_file_name):
                    tmp_file = open(tmp_file_name, 'w')
                    tmp_file.write("hhs\tjobs\tretail\tfires\tgov\tedu\twtcu\tmanu\n")
                else:
                    tmp_file = open(tmp_file_name, 'a')
                tmp_file.write("%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\t%6d\n" % tuple(
                                                    [tmpvalues[0:4].sum(), tmpvalues[4:16].sum(),
                                                     tmpvalues[4:7].sum(), tmpvalues[7:10].sum(), 
                                                     tmpvalues[10:13].sum()] + tmpvalues[13:16].tolist()))
            ####                                        
            for i in range(101, 125):
                newfile.write(line_template % (taz_id, i, self._get_value_for_zone(taz_id, zone_set, variables_list[i-101])))
        newfile.close()
        ####   
        tmp_file.close()
        ####   
        logger.end_block()
        return tm_input_file
    
    def _write_workplaces_to_files(self, person_set, tm_input_files):
        new_person_set = self.generate_workplaces(person_set)
        return self._write_workplaces_to_files_local(new_person_set, tm_input_files)
    
    def _write_workplaces_to_files_local(self, person_set, tm_input_files):
        home_zones = person_set.get_attribute("zone_id")
        job_zones = person_set.get_attribute("job_zone_id")
        ###
        person_idx = where(person_set.get_attribute("is_placed_non_home_based_worker_with_job"))[0]
        tmp_file_name = os.path.join(self.file_dir, 'workers_from_to_zones_propfac')
        if not os.path.exists(tmp_file_name):
            tmp_file = open(tmp_file_name, 'w')
            tmp_file.write("zone\tfrom\tto\n")
        else:
            tmp_file = open(tmp_file_name, 'a')
        tmpworkzones = ndimage.sum(ones(person_idx.size), labels=job_zones[person_idx], index=arange(1,938))
        tmphomezones = ndimage.sum(ones(person_idx.size), labels=home_zones[person_idx], index=arange(1,938))
        for z in [189, 97, 119, 107, 344, 181]:
            tmp_file.write("%4d\t%6d\t%6d\n" % (z, tmphomezones[z-1], tmpworkzones[z-1]))
        tmp_file.close()
        ###
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
