# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tools.explore_model import main

if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    ex = main()