# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.logger import logger
                
if __name__ == "__main__":
    logger.start_block("Pause simulation on travel model...")
    char = ''
    logger.log_status()
    while char.lower() != 'y':
        char = raw_input("Press 'y' when ready to continue:")
    logger.end_block()
