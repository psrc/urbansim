# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, sys
from opus_core.logger import logger

class RunDummyTravelModel():
    """Run a dummy travel model.  This is used in the test, where this is run in lieu of the Java code.
    """

    def run(self):
        """
        """
        logger.start_block("Starting RunDummyTravelModel.run(...)")
        
        print >> sys.stderr, "\nThis should also check if get_cache_data_into_matsim did something reasonable"
        
        logger.log_status('would normally run MATSim')
        
#        if not (sys.path == None) and len(sys.path) > 0:
#            module_path = sys.path[0]
#            logger.log_note("project path: %s" % module_path)
#        
#        in_file_name = os.path.join( module_path, "data", "travel_data_manipulated.csv" )
#        logger.log_note("open file : %s" % in_file_name)
#        file_in = open(in_file_name, 'r')
        out_file_name = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "tmp", "travel_data.csv" )
        logger.log_note("open file : %s" % out_file_name)
        file_out = open(out_file_name, 'w')
        
        # cbd_zone = "129"
        
        file_out.write("from_zone_id:i4,to_zone_id:i4,single_vehicle_to_work_travel_cost:f4\n")
        file_out.write("1,1,0.0\n")
        file_out.write("1,102,999.9999999999999\n")
        file_out.write("1,109,999.9999999999999\n")
        file_out.write("1,126,999.9999999999999\n")
        file_out.write("1,128,999.9999999999999\n")
        file_out.write("1,134,999.9999999999999\n")
        file_out.write("1,139,999.9999999999999\n")
        file_out.write("1,140,999.9999999999999\n")
        file_out.write("1,2,999.9999999999999\n")
        file_out.write("102,1,999.9999999999999\n")
        file_out.write("102,102,0.0\n")
        file_out.write("102,109,999.9999999999999\n")
        file_out.write("102,126,999.9999999999999\n")
        file_out.write("102,128,999.9999999999999\n")
        file_out.write("102,134,999.9999999999999\n")
        file_out.write("102,139,999.9999999999999\n")
        file_out.write("102,140,999.9999999999999\n")
        file_out.write("102,2,999.9999999999999\n")
        file_out.write("109,1,999.9999999999999\n")
        file_out.write("109,102,999.9999999999999\n")
        file_out.write("109,109,0.0\n")
        file_out.write("109,126,999.9999999999999\n")
        file_out.write("109,128,999.9999999999999\n")
        file_out.write("109,134,999.9999999999999\n")
        file_out.write("109,139,999.9999999999999\n")
        file_out.write("109,140,999.9999999999999\n")
        file_out.write("109,2,999.9999999999999\n")
        file_out.write("126,1,999.9999999999999\n")
        file_out.write("126,102,999.9999999999999\n")
        file_out.write("126,109,999.9999999999999\n")
        file_out.write("126,126,0.0\n")
        file_out.write("126,128,999.9999999999999\n")
        file_out.write("126,134,999.9999999999999\n")
        file_out.write("126,139,999.9999999999999\n")
        file_out.write("126,140,999.9999999999999\n")
        file_out.write("126,2,999.9999999999999\n")
        file_out.write("128,1,999.9999999999999\n")
        file_out.write("128,102,999.9999999999999\n")
        file_out.write("128,109,999.9999999999999\n")
        file_out.write("128,126,999.9999999999999\n")
        file_out.write("128,128,0.0\n")
        file_out.write("128,134,999.9999999999999\n")
        file_out.write("128,139,999.9999999999999\n")
        file_out.write("128,140,999.9999999999999\n")
        file_out.write("128,2,999.9999999999999\n")
        file_out.write("134,1,999.9999999999999\n")
        file_out.write("134,102,999.9999999999999\n")
        file_out.write("134,109,999.9999999999999\n")
        file_out.write("134,126,999.9999999999999\n")
        file_out.write("134,128,999.9999999999999\n")
        file_out.write("134,134,0.0\n")
        file_out.write("134,139,999.9999999999999\n")
        file_out.write("134,140,999.9999999999999\n")
        file_out.write("134,2,999.9999999999999\n")
        file_out.write("139,1,999.9999999999999\n")
        file_out.write("139,102,999.9999999999999\n")
        file_out.write("139,109,999.9999999999999\n")
        file_out.write("139,126,999.9999999999999\n")
        file_out.write("139,128,999.9999999999999\n")
        file_out.write("139,134,999.9999999999999\n")
        file_out.write("139,139,0.0\n")
        file_out.write("139,140,999.9999999999999\n")
        file_out.write("139,2,999.9999999999999\n")
        file_out.write("140,1,999.9999999999999\n")
        file_out.write("140,102,999.9999999999999\n")
        file_out.write("140,109,999.9999999999999\n")
        file_out.write("140,126,999.9999999999999\n")
        file_out.write("140,128,999.9999999999999\n")
        file_out.write("140,134,999.9999999999999\n")
        file_out.write("140,139,999.9999999999999\n")
        file_out.write("140,140,0.0\n")
        file_out.write("140,2,999.9999999999999\n")
        file_out.write("2,1,999.9999999999999\n")
        file_out.write("2,102,999.9999999999999\n")
        file_out.write("2,109,999.9999999999999\n")
        file_out.write("2,126,999.9999999999999\n")
        file_out.write("2,128,999.9999999999999\n")
        file_out.write("2,134,999.9999999999999\n")
        file_out.write("2,139,999.9999999999999\n")
        file_out.write("2,140,999.9999999999999\n")
        file_out.write("2,2,0.0\n")
       
        try:
            #file_in.close()
            file_out.close()
        except: logger.log_warning("file not closed")
        
        logger.end_block()

# called from opus via main!
if __name__ == "__main__":
    logger.enable_memory_logging()
    RunDummyTravelModel().run()    