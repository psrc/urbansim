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
