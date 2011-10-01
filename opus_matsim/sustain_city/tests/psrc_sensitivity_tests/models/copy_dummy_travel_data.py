# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import shutil
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
import opus_matsim.sustain_city.tests.psrc_sensitivity_tests as test_path
from opus_core import paths


class CopyDummyTravelData(AbstractTravelModel):
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
        #try: #tnicolai
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        # set travel data for test simulation
        if year == self.base_year+1:
            logger.log_status("Prepare copying pre-calculated MATSim travel data to OPUS_HOME tmp directory.")
            self.copy_dummy_travel_data()
        # use modified travel data for all following runs
        else:
            logger.log_status("Travel data is already copied in the first iteration.")

        logger.end_block()
        
    def copy_dummy_travel_data(self):
        ''' Copies pre-calculated MATSim travel costs, travel times and workplace accessibility into the 
            OPUS HOME tmp directory.
        '''
        # get sensitivity test path as an anchor to determine the location of the MATSim travel_data file
        #test_dir_path = test_path.__path__[0]

        # set source location
        travel_data_source = paths.get_opus_data_path_path('psrc_parcel_cupum_preliminary', 'MATSimTravelData', 'travel_data.csv' )
        if not self.travel_data_exsists( travel_data_source ):
            raise StandardError( 'Dummy MATSim travel data not fould! %s' % travel_data_source )
        workplace_accessibility_source = paths.get_opus_data_path_path('psrc_parcel_cupum_preliminary', 'MATSimTravelData', 'zones.csv' )
        if not self.travel_data_exsists( workplace_accessibility_source ):
            raise StandardError( 'Dummy MATSim travel data not fould! %s' % workplace_accessibility_source )
            
        # set destination location
        destination_dir = paths.get_opus_home_path( "opus_matsim", "tmp" )
        if not os.path.exists(destination_dir):
            try: os.mkdir(destination_dir)
            except: pass
        self.travel_data_destination = os.path.join( destination_dir, "travel_data.csv" )
        self.workplace_accessibility_destination = os.path.join( destination_dir, "zones.csv" )
        
        logger.log_status("Copying dummy travel data:")
        logger.log_status("Source: %s" % travel_data_source)
        logger.log_status("Destination %s:" % self.travel_data_destination)
        
        # copy travel data
        shutil.copy (travel_data_source, self.travel_data_destination)
        if os.path.isfile (self.travel_data_destination): 
            logger.log_status("Copying successful ...")
        else: 
            raise StandardError("Test travel data travel_data_destination not copied!")
        
        logger.log_status("Copying dummy workplace accessibility indicators:")
        logger.log_status("Source: %s" % workplace_accessibility_source)
        logger.log_status("Destination %s:" % self.workplace_accessibility_destination)
        
        # copy workplace accessibility indicators
        shutil.copy (workplace_accessibility_source, self.workplace_accessibility_destination)
        if os.path.isfile (self.workplace_accessibility_destination): 
            logger.log_status("Copying successful ...")
        else: 
            raise StandardError("Test travel data workplace_accessibility_destination not copied!")  
        
    def travel_data_exsists(self, travel_data):
        if not os.path.exists( travel_data ):
            raise StandardError("Test travel data not found: %s" % travel_data)
            return False
        else: return True

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

    CopyDummyTravelData().run(resources, options.year)
    
    