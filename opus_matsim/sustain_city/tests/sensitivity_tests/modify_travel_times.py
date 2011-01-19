# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_matsim.sustain_city.tests.sensitivity_tests.export_base_year_travel_data import ExportTravelData
from opus_matsim.sustain_city.tests.sensitivity_tests.get_indices import GetIndices
from opus_matsim.sustain_city.tests.sensitivity_tests.get_test_travel_data_into_cache import GetTestTravelDataIntoCache
import opus_matsim.sustain_city.tests as test_dir
from opus_core.store.csv_storage import csv_storage
from urbansim.datasets.travel_data_dataset import TravelDataDataset
import numpy

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
        self.base_year = self.travel_model_configuration['base_year']
        
        # set output directory for travel data
        self.travel_data_dir = os.path.join( os.environ['OPUS_HOME'], 'opus_matsim', 'tmp')

        # for debugging
        #try: #tnicolai
        #    import pydevd
        #    pydevd.settrace()
        #except: pass

        # set travel data for test simulation
        if year == self.base_year+1:
            logger.log_status('Exporting travel_data from base_year_cache to %s' % self.travel_data_dir)
            self.export_travel_data(None)
            logger.log_status("Modifying travel times.") # comment out for base scenario
            self.modify_travel_time()                    # comment out for base scenario
            logger.log_status("Finished modifying...")   # comment out for base scenario
            #logger.log_status('Integrating test travel data into UrbanSim cache for next simulation year.')
            #self.integrate_test_travel_data(year)
            #logger.log_status("Finished integrating...")
            #logger.log_status("Copying updated (integrated) travel data from cache to OPUS_HOME tmp directory.")
            #self.export_travel_data(year+1)
            #logger.log_status("Finished copying...") 
        # use modified travel data for all following runs
        else:
            logger.log_status("Travel data was modified before. So there is nothing to do...")

        logger.end_block()
        
    def export_travel_data(self, year):
        """ Exports the travel data from the base year data into the working directory
        """
        # export travel data for base year + 1 (2000 + 1),
        # because pre-computed travel costs will be applied for that year 
        # (see above: integrate_test_travel_data)
        export = ExportTravelData(self.travel_data_dir, year)
        export.export()
        
    def integrate_test_travel_data(self, year):
        ''' integrate modified travel times and 
            pre-computed MATSim travel cost into
            UrbanSim travel data cache
        '''
        
        # integrate pre-computed MATSim travel cost into cache.
        # changes will be applied for the next year (current year +1)
        GetTestTravelDataIntoCache().run(self.config, year)
        
    def modify_travel_time(self):
        """ Modifies the travel times to the cbd. The preferered zone (20)
            gets minimum travel times, all other zones get high travel times.
            
            @old version
            Modifies the travel times from zone to zone.
            For zone 20 the travel times to all other zones is set to min_travel_time.
            For all other zones the trvel time will be set on 31min if the origin travel time
            is less than 30min, otherwise it's not modified.
        """
        
        # using default cbd 
        cbd = 129
        # set the preferred zone
        preferential_zone = 20
        # set travel times for the preferered zone and other zones
        min_travel_time = '0.40'    # time in minutes
        # max_travel_time = '121.02'  # time in minutes
        travel_time_border = 30.0   # time in minutes
        offset = 2.0                # time in minutes
        
        
        logger.log_status("Preferential zone with travel time = 40msec is set to: %s" % preferential_zone)
        logger.log_status("The travel time border of other zones is set to %f" % travel_time_border)
        logger.log_status("Offset to travel time border is %f" % offset)
        
        travel_data = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "tmp", "travel_data.csv" )
        if not self.travel_data_exsists(travel_data):
            raise StandardError('Travel data not found! %s' % travel_data)
            
        travel_cost_list = self.get_travel_cost_matrix()
            
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
            travel_cost_value = travel_cost_list[from_zone_id][to_zone_id]
            travel_times_value = float(row[index_travel_times].strip('\r\n'))
            
            # new version (compute travel times from/to cbd. If preferential zone occurs set min travel times.
            # otherwise check if the travel times of other zones from/to cbd is lower than 30min than set it to travel times higher than 30min)
            # get all zones from and to cbd
            if( from_zone_id == cbd ) or (to_zone_id == cbd ):
                # if its the the preferaential zone and the cbd set minimum travel times
                if ((from_zone_id == preferential_zone) and (to_zone_id == cbd)) or\
                   ((from_zone_id == cbd) and (to_zone_id == preferential_zone)):
                    row[index_travel_times] = min_travel_time
                
                # if its the cbd itself don't change anything
                elif (from_zone_id == cbd) and (to_zone_id == cbd):
                    pass
                
                # if zone form/to cbd is other then the preferential zone set the travel times 
                # higher than 30min (when the travel times are lower than 30min)
                elif ((from_zone_id != preferential_zone) and (to_zone_id == cbd)) or\
                     ((from_zone_id == cbd) and (to_zone_id != preferential_zone)):
                    if travel_times_value <= travel_time_border:
                        row[index_travel_times] = str(travel_time_border + offset)
            
            #old version (Set travel times from preferential zone to all other zone to min travel times. For all other zones set travel times
            # higher than 30min if they have less than 30min)
            ## travel time from zone 20 to other zone or from other zone to zone 20 is set to 40sec.
            #if (from_zone_id == preferential_zone) or (to_zone_id == preferential_zone):
            #    row[index_travel_times] = min_travel_time
            #    # travel time from/to zone other than 20 is set to 30min+offset if the travel time was originally lower than 30min
            #elif travel_times_value <= travel_time_border:
            #    row[index_travel_times] = str(travel_time_border + offset)
        
            # append modified row to the new travel data content
            str_list.append( row[index_from_zone].strip('\r\n') +','+ row[index_to_zone].strip('\r\n') +','+ row[index_travel_times].strip('\r\n') + ',' + str(travel_cost_value) +'\r\n')

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