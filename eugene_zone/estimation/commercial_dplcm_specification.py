# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

all_variables = [   
    ('lvalue = ln(zone.aggregate(pseudo_building.avg_value))', 'BLVALUE')
                 ]
#commercial DPLCM estimate with:
#python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.commercial_dplcm_specification -m "commercial_development_project_location_choice_model"
specification = {  #commercial
'_definition_': all_variables,
-2:
    [
     'lvalue',
    ],
}
