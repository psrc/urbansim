# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 


import os
from opus_core.configuration import Configuration
from urbansim.synthesize_jobs import SynthesizeJobs
from time import time

#WARNING: THIS IS LIKELY OBSOLETE AND WILL NOT WORK

config = {
    'output_database_name':'washtenaw_estimation_synthesized_output',

    'gridcells':'gridcells',
    'gridcells_output':'gridcells',
    'jobs':'jobs',
    'jobs_by_zone_by_sector':'jobs_by_zone_by_sector',
    'jobs_output':'jobs',
    
    'sector_names_and_ids':(
            ('ag',   1),
            ('mfg',  2),
            ('tcu',  3),
            ('whl',  4),
            ('rtl',  5),
            ('fire', 6),
            ('srv',  7),
            ('pub',  8)
        ),
        
    'building_type_column_names_and_ids_and_home_based':(
            ('COM', 1, False),
            ('GOV', 2, False),
            ('IND', 3, False),
            ('RES', 4, True)
        ),
    
    'store':{
        'type':'sql_storage',
        'database_name':'washtenaw_class',
        'drop_database_first':False,
        },
    }
    
job_configuration = Configuration(config)

print "Beginning employment synthesis process."

before = time()
try:
    SynthesizeJobs().synthesize_employment_data(config)
    
except Exception, val:
    after = time()
    delta = after-before
    print "Employment synthesis failed after %s seconds." % round(delta, 2)
    raise Exception, val
    
after = time()

delta = after-before

print "Employment synthesis complete in %s seconds." % round(delta, 2)