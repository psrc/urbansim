# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington and Kai Nagel
# See opus_core/LICENSE

import os
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.export_storage import ExportStorage
from opus_core.store.csv_storage import csv_storage 
import opus_matsim.sustain_city.tests.psrc_sensitivity_tests.config as test_path

class ExportTravelData(object):
    ''' Export travel data from UrbanSim cache into OPUS_HOME
        tmp directory.
        The Export can be done from a given sinmulation year or
        the base_year_cache (if year == None).
    '''

    def __init__(self, output_dir=None,  year=None):
        ''' Constructor
        '''
        # get working path as an anchor e.g. to determine the config file location.
        self.working_path = test_path.__path__[0]
        print "Working path: %s" % self.working_path
        # get config file location
        self.config_file = os.path.join( self.working_path, 'psrc_modified_without_matsim_scenario.xml')
        
        # get seattle_parcel configuration
        config = XMLConfiguration( self.config_file ).get_run_configuration( "PSRC_baseline" )
        
        self.input_storage = None
        
        # get first simulation year
        self.year = year
        if self.year == None:
            self.year = config['base_year']
            base_year_data_path = os.path.join( os.environ['OPUS_DATA_PATH'], 'psrc_parcel', 'base_year_data')
            attribute_cache = AttributeCache(cache_directory=base_year_data_path)
            self.input_storage = attribute_cache.get_flt_storage_for_year(self.year)
        else:
            attribute_cache = AttributeCache().get_flt_storage_for_year(self.year)
            self.input_storage = attribute_cache
        
        # get output dir path
        output_directory = output_dir
        if output_directory == None:
            # set deafult
            output_directory = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp')
        if not os.path.exists( output_directory ):
            try: os.mkdir( output_directory )
            except: pass
        
        # init 
        self.csv_data_path = output_directory # os.path.join(output_directory, 'travel_data_dir')
        
    def export(self):
        ''' Run export process
        '''
        output_storage = csv_storage(storage_location = self.csv_data_path)
        
        ExportStorage().export_dataset(
                dataset_name = 'travel_data',
                in_storage = self.input_storage,
                out_storage = output_storage,
        )
        
if __name__ == "__main__":
    etd = ExportTravelData(None,None)
    etd.export()