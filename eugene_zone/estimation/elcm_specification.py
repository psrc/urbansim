#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

all_variables = [   
    ('lsfi = ln(urbansim_zone.zone.industrial_sqft)', 'BLSFI'),
    ('lsfc = ln(urbansim_zone.zone.commercial_sqft)', 'BLSFC'),
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
     #'lsfi',
     'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
2:    
    [
     'lsfi', 
     #'lindjobs',
     #'ldu',
     'lavinc',
     'ljobs',
     'lcbd'
    ],
3:
    [
     'lsfi', 
     'lindjobs',
     #'ljobs',
     #'ldu',
     #'lavinc',
     #'lcbd'
     ],
4:
    [
     'lsfi',
     #'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
5:
    [
     'lsfi',
     'lindjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd'
    ],
6:
    [
     'lsfi', 
     #'lindjobs',
     'ljobs',
     #'ldu',
     #'lavinc',
     #'lcbd'
     ],
7:
    [
     'lsfi',
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
     #'lsfc',
     #'lcomjobs',
     'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
2:
    [
     #'lsfc',
     #'lcomjobs',
     'ljobs',
     'ldu',
     #'lavinc',
     'lcbd',
     #'lemp30'
    ],
3:
    [
     'lsfc',
     'lcomjobs',
     'ljobs',
     #'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
4:
    [
     'lsfc',
     'lcomjobs',
     #'ljobs',
     'ldu',
     #'lavinc',
     'lcbd',
     #'lemp30'
    ],
5:
    [
     #'lsfc',
     'lcomjobs',
     #'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],
6:
    [
     #'lsfc',
     'lcomjobs',
     #'ljobs',
     'ldu',
     #'lavinc',
     #'lcbd',
     #'lemp30'
    ],
7:
    [
     #'lsfc',
     'lcomjobs',
     'ljobs',
     'ldu',
     'lavinc',
     'lcbd',
     #'lemp30'
    ],

8:
    [
     'lsfc',
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
