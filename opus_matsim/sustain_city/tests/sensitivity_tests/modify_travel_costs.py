# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys
import shutil
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_matsim.sustain_city.tests.sensitivity_tests.get_indices import GetIndices
import opus_matsim.sustain_city.tests as test_path
from opus_core import paths


class ModifyTravelCosts(AbstractTravelModel):
    """Runs a dummy travel model for testing reasons mnipulating travel costs.
    """

    def run(self, config, year):
        """ This class simulates a MATSim run. Therefore it copies 
            real travel data into the OPUS_HOME and modifies the 
            travel cost entries.
        """        
        logger.start_block("Starting ModifyTravelCosts.run(...)")

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
            self.copy_pre_calculated_MATSim_travel_costs()
            logger.log_status("Modifying travel costs.")
            self.modify_travel_costs()                  # comment out for base scenario
            logger.log_status("Finished modifying...")  # comment out for base scenario
        # use modified travel data for all following runs
        else:
            logger.log_status("Travel data was modified before. So there is nothing to do...")

        logger.end_block()
        
    def copy_pre_calculated_MATSim_travel_costs(self):
        ''' Copies pre-calculated MATSim travel costs into the 
            OPUS HOME tmp directory.
        '''
        # get sensitivity test path as an anchor to determine the location of the MATSim travel_data file
        test_dir_path = test_path.__path__[0]
        
        # set source location
        travel_data_source = os.path.join( test_dir_path, 'data', 'travel_cost', "travel_data.csv" )
        if not self.travel_data_exsists( travel_data_source ):
            print('Pre-computed MATSim travel data not fould! %s' % travel_data_source)
            sys.exit()
            
        # set destination location
        destination_dir = paths.get_opus_home_path("opus_matsim", "tmp")
        if not os.path.exists(destination_dir):
            try: os.mkdir(destination_dir)
            except: pass
        travel_data_destination = os.path.join( destination_dir, "travel_data.csv" )
        
        logger.log_status("Copying pre-calculated MATSim travel data:")
        logger.log_status("Source: %s" % travel_data_source)
        logger.log_status("Destination %s:" % travel_data_destination)
        
        # copy travel data
        shutil.copy (travel_data_source, travel_data_destination)
        if os.path.isfile (travel_data_destination): 
            logger.log_status("Copying successful ...")
        else: 
            raise Exception("Test travel data not copied!")
            sys.exit()
        
    def modify_travel_costs(self):
        ''' Modifies the travel costs to the cbd. The preferered zone (20)
            gets low costs, all other zones get high costs.
        '''
        
        # using default cbd 
        cbd = '129'
        preferential_zone = '20'
        low_travel_cost = '3.47'
        high_travel_cost = '1689.19'
        
        logger.log_status("Set cbd to %s" %cbd)
        logger.log_status("Preferential zone with travel cost = 3.47 is set to: %s" % preferential_zone)
        logger.log_status("The travel costs of other zones is set to %s" % high_travel_cost)
        
        travel_data = paths.get_opus_home_path('opus_matsim', 'tmp', 'travel_data.csv')
        if not self.travel_data_exsists(travel_data):
            raise Exception('Travel data not found! %s' % travel_data)
            
        in_file = open(travel_data, 'r')
        str_list = []
        # read header of travel data to get the indices of the colums (from_zone, to_zone, single_vehicle_travel_cost)
        line = in_file.readline()
        # init indices
        get_indices = GetIndices(line)
        index_from_zone = get_indices.get_from_zone_index()
        index_to_zone   = get_indices.get_to_zone_index()
        index_travel_costs = get_indices.get_single_vehicle_to_work_travel_cost_index()
        number_of_colums = get_indices.get_number_of_colums()
        
        
        # prepare header line for the output file
        row = line.split(',')
        str_list.append( row[index_from_zone].strip('\r\n') +','+ row[index_to_zone].strip('\r\n') +','+ row[index_travel_costs].strip('\r\n') +'\r\n')
        
        # get first line of the table content
        line = in_file.readline()
        
        # replaces the travel costs for every occurence of cbd according to origin zone
        while line:
            row = line.split(",")
            # consistency check
            if len(row) != number_of_colums:
                print('Error in number of colums: %s' %row)
                sys.exit()
            
            # get all zones from and to cbd
            if (row[index_from_zone] == cbd) or (row[index_to_zone] == cbd):
                # if its the travel costs beween the preferaential zone and the cbd set low costs
                if ((row[index_from_zone] == preferential_zone) and (row[index_to_zone] == cbd)) or\
                   ((row[index_from_zone] == cbd) and (row[index_to_zone] == preferential_zone)):
                    row[index_travel_costs] = low_travel_cost
                    # append modified row to the new travel data content
                    str_list.append( row[index_from_zone] +','+ row[index_to_zone] +','+ row[index_travel_costs] +'\n')
                
                # if its the cbd itself don't change anything
                elif (row[index_from_zone] == cbd) and (row[index_to_zone] == cbd):
                    # append unmodified row to the new travel data content
                    str_list.append( line )
                
                # if its another zone than the prefrerred zone or the cbd set high costs
                elif ((row[index_from_zone] != preferential_zone) and (row[index_to_zone] == cbd)) or\
                   ((row[index_from_zone] == cbd) and (row[index_to_zone] != preferential_zone)):
                    row[index_travel_costs] = high_travel_cost
                    # append modified row to the new travel data content
                    str_list.append( row[index_from_zone] +','+ row[index_to_zone] +','+ row[index_travel_costs] +'\n')
                    
            # otherwise don't change anything
            else:
                # append unmodified row to the new travel data content
                str_list.append( line )
            # get next line
            line = in_file.readline()
        
        # finished modifying traval data
        in_file.close()
        # now write new travel data ono disc
        out_file = open(travel_data, 'w')
        logger.log_status("Copying modified travel data onto disc.")
        for row in str_list:
            out_file.write(row)
        out_file.close();
        logger.log_status("Finished copy process.")
        
    def travel_data_exsists(self, travel_data):
        if not os.path.exists( travel_data ):
            raise Exception("Test travel data not found: %s" % travel_data)
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

    ModifyTravelCosts().run(resources, options.year)
    
    