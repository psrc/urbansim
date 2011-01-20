# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tools.start_estimation import main
    
if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    er = main()
