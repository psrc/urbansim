# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import shutil
from opus_core.resources import Resources
from opus_core.logger import logger
from opus_matsim.sustain_city.tests.psrc_sensitivity_tests.models.copy_dummy_travel_data import CopyDummyTravelData
from opus_matsim.sustain_city.tests.psrc_sensitivity_tests.models.get_indices import GetIndices



class CopyDummyTravelDataWithModWPA(CopyDummyTravelData):
    """Copies dummy travel data for testing reasons into opus home tmp directory to replace the
        travel data in urbansim data set.
    """

    def run(self, config, year):
        """ This class simulates a MATSim run copying a manipulated 
            travel data into opus home tmp directory
        """        
        logger.start_block("Starting CopyDummyTravelData.run(...)")

        self.config = config
        # get travel model parameter from the opus dictionary
        self.travel_model_configuration = config['travel_model_configuration']
        self.base_year = self.travel_model_configuration['base_year']
        
        # for debugging
        try: #tnicolai
            import pydevd
            pydevd.settrace()
        except: pass
        
        # set travel data for test simulation
        if year == self.base_year+1:
            logger.log_status("Prepare copying pre-calculated MATSim travel data to OPUS_HOME tmp directory.")
            self.copy_dummy_travel_data()
        # use modified travel data for all following runs
        else:
            logger.log_status("Travel data is already copied in the first iteration.")

        logger.end_block()
        
    def modify_workplace_accessibility(self):
        
        study_zone = 908
        
        # set workplace accessibility for the preferered zone and other zones
        min_wpa = '3.0'    # time in minutes
        max_wpa = '15.0'    # travel const in ???
        
        logger.log_status("Zone ID study zone = %s" %study_zone)
        
        in_file = open(self.workplace_accessibility_destination, 'r')
        str_list = []
        # read header of travel data to get the indices of the colums (from_zone, to_zone, single_vehicle_travel_time)
        line = in_file.readline()
        # init indices
        get_indices = GetIndices(line)
        index_zone_id = get_indices.get_zone_id_index()
        index_wpa   = get_indices.get_workplace_asseccibility_index()
        number_of_colums = get_indices.get_number_of_colums()
        
        # prepare header line for the output file
        row = line.split(',')
        str_list.append( row[index_zone_id].strip('\r\n') +','+ row[index_wpa].strip('\r\n') +'\r\n')
        
        # get first line of the table content
        line = in_file.readline()
        
        # replaces the travel times as decribed above...
        while line:
            row = line.split(',')
            # consistency check
            if len(row) != number_of_colums:
                raise StandardError('Error in number of colums: %s' %row)
            
            zone_id = int(row[index_zone_id].strip('\r\n'))
            
            if zone_id == study_zone:
                row[index_wpa] = max_wpa
            else:
                row[index_wpa] = min_wpa
                
            # append modified row to the new travel data content
            str_list.append( row[index_zone_id].strip('\r\n') +','+ row[index_wpa].strip('\r\n') +'\r\n')

            line = in_file.readline()
        
        # finished modifying traval data
        in_file.close()
        # now write new travel data onto disc
        out_file = open(self.workplace_accessibility_destination, 'w')
        logger.log_status("Copying modified travel data onto disc.")
        for row in str_list:
            out_file.write(row)
        out_file.close();
        logger.log_status("Finished copy process.")

# called from the framework via main!
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()

    resources = Resources(get_resources_from_file(options.resources_file_name))

    CopyDummyTravelDataWithModWPA().run(resources, options.year)
    
    