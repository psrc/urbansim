# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

all_variables = [   
    ('lcjs = ln(urbansim_zone.zone.total_commercial_job_space)', 'BLSFC'),
    ('lijs = ln(urbansim_zone.zone.total_industrial_job_space)', 'BLSFI'),
    ('ldu = ln(urbansim_zone.zone.residential_units)', 'BLDU'),
    ('lavinc = ln(urbansim.zone.average_income)','BLAVINC'),
    ('ljobs = ln(urbansim.zone.number_of_jobs)', 'BLJOBS'), 
    ('lindjobs = ln(urbansim_zone.zone.number_of_industrial_jobs)', 'BLIJOBS'), 
    ('lcbd = ln(zone.travel_time_to_cbd)','BCBD'),
    ('lcomjobs = ln(urbansim_zone.zone.number_of_commercial_jobs)', 'BLCJOBS'),
    ('lemp30 = ln(eugene.zone.employment_within_30_minutes_travel_time_hbw_am_drive_alone)', 'BLEMP30'),
    ('lpop = ln(zone.aggregate(household.persons))', 'BLPOP')
                 ]
specification ={}

#industrial ELCM estimate with:
#python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.elcm_specification -m "employment_location_choice_model" --group='industrial'
specification['industrial'] = { #industrial
'_definition_': all_variables,
1:
    [
     #'lijs',
     'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
2:    
    [
     'lijs', 
     #'lindjobs',
     #'ldu',
     'lavinc',
     'ljobs',
     'lcbd'
    ],
3:
    [
#     'lijs', 
     'lindjobs',
     #'ljobs',
     #'ldu',
     #'lavinc',
     #'lcbd'
     ],
4:
    [
     'lijs',
     #'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
5:
    [
     'lijs',
     'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
6:
    [
#     'lijs', 
     'lindjobs',
 #    'ljobs',
     #'ldu',
     #'lavinc',
     #'lcbd'
     ],
7:
    [
     'lijs',
     'lindjobs',
     #'ljobs',
     'ldu',
     #'lavinc',
     'lcbd'
    ]
}

#commercial ELCM estimate with:
#python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.elcm_specification -m "employment_location_choice_model" --group='commercial'
specification['commercial'] = {  #commercial
'_definition_': all_variables,
1:
    [
     #'lcjs',
     #'lcomjobs',
     'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
2:
    [
     #'lcjs',
     #'lcomjobs',
     'ljobs',
     'ldu',
     #'lavinc',
     'lcbd',
     #'lemp30'
    ],
3:
    [
     'lcjs',
     'lcomjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
4:
    [
     'lcjs',
     'lcomjobs',
     #'ljobs',
     'ldu',
     #'lavinc',
     'lcbd',
     #'lemp30'
    ],
5:
    [
     #'lcjs',
     'lcomjobs',
     #'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
6:
    [
     #'lcjs',
     'lcomjobs',
     #'ljobs',
     'ldu',
     #'lavinc',
     #'lcbd',
     #'lemp30'
    ],
7:
    [
     #'lcjs',
     'lcomjobs',
     'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],

8:
    [
     'lcjs',
     #'lcomjobs',
     'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ]
}

#home-based ELCM estimate with:
#python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.elcm_specification -m "employment_location_choice_model" --group='home_based'
specification['home_based'] = { #home-based
'_definition_': all_variables,
-2:
    [
     'lpop',
     'ldu',
     'lcomjobs',
     'lindjobs',
     'lcbd',
     #'lemp30'
    ],
}
