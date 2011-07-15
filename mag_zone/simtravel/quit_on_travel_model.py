# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import sys
from opus_core.logger import logger

if __name__ == "__main__":
    returncode = 10
    logger.log_status("Quit simulation on travel model with exit code %s" % returncode)
    sys.exit(returncode)
