#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from inprocess.configurations.xml_configuration import XMLConfiguration
# from psrc_parcel.estimation.run_estimation import EstimationRunner
from inprocess.configurations.gui_estimation_runner import EstimationRunner

inprocess_dir = __import__('inprocess').__path__[0]
parcelfile = os.path.join(inprocess_dir, 'configurations', 'projects', 'psrc_parcel.xml')
xml_config = XMLConfiguration(parcelfile)
estimation_section = xml_config.get_estimation_section()
estimation_config = estimation_section['estimation_config']

# TODO: put save_estimation results etc into config
for model_name in estimation_config['models_to_estimate']:
    model_config = estimation_config['model_parameters'][model_name]
    model = (model_config['abbreviation'], model_config['full_name'])
    if 'location' in model_config:
        model = model , (model_config['location'], model_config['add_member_prefix'])
    specification = xml_config.get_estimation_specification(model_config['full_name'])
    er = EstimationRunner()
    er.run_estimation(estimation_config, model, specification, save_estimation_results=True, diagnose=False)
    
