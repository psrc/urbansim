# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

all_variables = [   
    ('lvalue = ln(zone.aggregate(pseudo_building.avg_value))', 'BLVALUE')
                 ]

#residential DPLCM estimate with:
#python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.residential_dplcm_specification -m "residential_development_project_location_choice_model"
specification = { # residential
'_definition_': all_variables,
-2:
    [
     'lvalue',
    ],
}
