# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
import opus_matsim.sustain_city.tests as test_dir
from opus_core.store.csv_storage import csv_storage
from urbansim.datasets.travel_data_dataset import TravelDataDataset
import numpy
from opus_matsim.sustain_city.tests.psrc_sensitivity_tests.models.export_base_year_travel_data import ExportTravelData
from opus_matsim.sustain_city.tests.psrc_sensitivity_tests.models.get_indices import GetIndices

class ModifyTravelTimes(AbstractTravelModel):
    '''Runs a dummy travel model for testing reasons manipulating travel times.
    '''
        
    def run(self, config, year):
        """ This class simulates a MATSim run. Therefore it copies 
            real travel data into the OPUS_HOME and modifies the 
            entries in the following runs.
        """        
        logger.start_block("Starting RunDummyTravelTimeTravelModel.run(...)")

        self.config = config
        # get travel model parameter from the opus dictionary
        self.travel_model_configuration = config['travel_model_configuration']
        
        self.first_year = 2001 # TODO make configurable (bayeyear + 1)
        
        # set output directory for travel data
        self.travel_data_dir = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp')

        # for debugging
        #try: #tnicolai
        #    import pydevd
        #    pydevd.settrace()
        #except: pass

        # set travel data for test simulation
        if year == self.first_year:
            logger.log_status('Exporting travel_data from base_year_cache to %s' % self.travel_data_dir)
            self.export_travel_data(None)
            logger.log_status("Modifying travel data.")
            self.modify_travel_data()   
            logger.log_status("Finished modifying...")  
        else:
            logger.log_status("Travel data was modified before. Nothing to do...")

        logger.end_block()
        
    def export_travel_data(self, year):
        """ Exports the travel data from the base year data into the working directory
        """
        # export travel data for base year + 1 (2000 + 1),
        # because pre-computed travel costs will be applied for that year 
        # (see above: integrate_test_travel_data)
        export = ExportTravelData(self.travel_data_dir, year)
        export.export()
        
    def modify_travel_data(self):
        """ Modifies the travel times and costs between cbd and study zone 909
            
            @old version
            Modifies the travel times from zone to zone.
            For zone 20 the travel times to all other zones is set to min_travel_time.
            For all other zones the trvel time will be set on 31min if the origin travel time
            is less than 30min, otherwise it's not modified.
        """
        
        # using default cbd 
        cbd = 129
        # set the preferred zone
        study_zone = 908
        # set travel times for the preferered zone and other zones
        min_travel_time = '0.40'    # time in minutes
        min_travel_cost = '3.47'    # travel const in ???
        
        logger.log_status("Set the following travel time and cost between cbd and study zone:")
        logger.log_status("Zone ID cbd = %s" %cbd)
        logger.log_status("Zone ID study zone = %s" %study_zone)
        logger.log_status("Travel time = %s" %min_travel_time)
        logger.log_status("Travel cost = %s" %min_travel_cost)
        
        travel_data = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp', "travel_data.csv" )
        if not self.travel_data_exsists(travel_data):
            raise StandardError('Travel data not found! %s' % travel_data)
            
        in_file = open(travel_data, 'r')
        str_list = []
        # read header of travel data to get the indices of the colums (from_zone, to_zone, single_vehicle_travel_time)
        line = in_file.readline()
        # init indices
        get_indices = GetIndices(line)
        index_from_zone = get_indices.get_from_zone_index()
        index_to_zone   = get_indices.get_to_zone_index()
        index_travel_times = get_indices.get_am_single_vehicle_to_work_travel_time_index()
        index_travel_costs = get_indices.get_single_vehicle_to_work_travel_cost_index()
        number_of_colums = get_indices.get_number_of_colums()
        
        # prepare header line for the output file
        row = line.split(',')
        str_list.append( row[index_from_zone].strip('\r\n') +','+ row[index_to_zone].strip('\r\n') +','+ row[index_travel_times].strip('\r\n') + ',' + row[index_travel_costs].strip('\r\n') +'\r\n')
        
        # get first line of the table content
        line = in_file.readline()
        
        # replaces the travel times as decribed above...
        while line:
            row = line.split(',')
            # consistency check
            if len(row) != number_of_colums:
                raise StandardError('Error in number of colums: %s' %row)
                
            from_zone_id = int(row[index_from_zone].strip('\r\n'))
            to_zone_id = int(row[index_to_zone].strip('\r\n'))
            
            
            # just sets the travel time and cost from cbd2studyzone and 
            # from stuyzone2cbd to the defined values above
            if (from_zone_id == cbd and to_zone_id == study_zone):
                row[index_travel_times] = min_travel_time
                row[index_travel_costs] = min_travel_cost
            
            elif (from_zone_id == study_zone and to_zone_id == cbd):
                row[index_travel_times] = min_travel_time
                row[index_travel_costs] = min_travel_cost
        
            # append modified row to the new travel data content
            str_list.append( row[index_from_zone].strip('\r\n') +','+ row[index_to_zone].strip('\r\n') +','+ row[index_travel_times].strip('\r\n') + ',' + row[index_travel_costs].strip('\r\n') +'\r\n')

            line = in_file.readline()
        
        # finished modifying traval data
        in_file.close()
        # now write new travel data onto disc
        out_file = open(travel_data, 'w')
        logger.log_status("Copying modified travel data onto disc.")
        for row in str_list:
            out_file.write(row)
        out_file.close();
        logger.log_status("Finished copy process.")
    
    def get_travel_cost_matrix(self):
        ''' Returns the pre-calculated MATSim travel costs as 2d list
        '''
        # get sensitivity test path
        test_dir_path = test_dir.__path__[0]
        
        input_directory = os.path.join( test_dir_path, 'data', 'travel_cost')
        print "input_directory: %s" % input_directory
        # check source file
        if not os.path.exists( input_directory ):
            print 'File not found! %s' % input_directory
            sys.exit()
        table_name = 'travel_data'
        travel_data_attribute = 'single_vehicle_to_work_travel_cost'
        # location of pre-calculated MATSim travel costs
        in_storage = csv_storage(storage_location = input_directory)
        # create travel data set (travel costs)
        travel_data_set = TravelDataDataset( in_storage=in_storage, in_table_name=table_name )
        travel_data_attribute_mat = travel_data_set.get_attribute_as_matrix(travel_data_attribute, fill=999)
        # travel cost matris as 2d array
        travel_list = numpy.atleast_2d(travel_data_attribute_mat).tolist()
        
        return travel_list
        
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

    ModifyTravelTimes().run(resources, options.year)