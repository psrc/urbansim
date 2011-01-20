# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# estimate REPM with:

# python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.repm_specification -m "real_estate_price_model"

all_variables = [   
    ('lcomjobs = ln(pseudo_building.commercial_job_spaces)', 'BLCJ'),
    ('lindjobs = ln(pseudo_building.industrial_job_spaces)', 'BLIJ'),
    ('lgovjobs = ln(pseudo_building.governmental_job_spaces)', 'BLGJ'),
    ('ldu = ln(pseudo_building.residential_units)', 'BLDU'),
            ]


specification = {
        # This is just a toy specification.
        '_definition_': all_variables,
        1: # commercial
            ['constant',
             'lcomjobs'
             ],
        2: # governmental
            ['constant',
             'lgovjobs'
             ],
        3: # industrial
            ['constant',
             'lindjobs'
             ],
        4: # residential
            ['constant',
             'ldu'
             ]
        }
