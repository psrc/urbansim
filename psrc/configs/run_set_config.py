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

import os
from opus_core.configuration import Configuration


class RunSetConfig(Configuration):
    """Configuration to start multiple runs in parallel
    """
    def __init__(self):
        self['run_set'] = {
                'baseline':'psrc.configs.baseline_copied_travel_data',
                'discounted_travel_data':'psrc.configs.baseline_discounted_travel_data',
                'inflated_travel_data':'psrc.configs.baseline_inflated_travel_data',
                }
        self['travel_data_directory_to_copy'] = '/urbansim_cache/run_1850.2007_01_15_17_03/'  #'/projects/urbansim5/urbansim_cache/run_1849.2007_01_15_16_09/'
