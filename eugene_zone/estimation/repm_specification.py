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

# estimate REPM with:

# python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.repm_specification -m "real_estate_price_model"

all_variables = [   
    ('ljobs = ln(pseudo_building.job_spaces)', 'BLJ'),
    ('ldu = ln(pseudo_building.residential_units)', 'BLDU'),
            ]


specification = {
        # This is just a toy specification.
        '_definition_': all_variables,
        1: # commercial
            ['constant',
             'ljobs'
             ],
        2: # governmental
            ['constant',
             'ljobs'
             ],
        3: # industrial
            ['constant',
             'ljobs'
             ],
        4: # residential
            ['constant',
             'ldu'
             ]
        }