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

from randstad.estimation.my_estimation_config import my_configuration
from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module


#model = ("HLCM", "household_location_choice_model") 
#model = ("ELCM", "employment_location_choice_model", "industrial")
#model = ("ELCM", "employment_location_choice_model", "commercial")
##model = ("ELCM", "employment_location_choice_model", "home_based") #disabled because jobs_for_estimation_home_based has no records
#model = ("LUDLCM", "landuse_development_location_choice_model")
model = ("HPM", "housing_price_model")
##model = ("RLSM", "residential_land_share_model") ##TODO

type = None
if len(model) > 2:
    type = model[2]
if type is None:
    exec("from randstad.estimation.%s_estimation_config import run_configuration" % model[0].lower())
    run_configuration = update_controller_by_specification_from_module(
                        run_configuration, model[1],
                        "%s_specification" % model[0])
else:
    exec("from randstad.estimation.%s_estimation_config import %s_configuration as config" % (model[0].lower(),
          model[0].lower()))
    conf = config(type)
    run_configuration = conf.get_configuration(specification_module="randstad.estimation.%s_specification" % model[0])
run_configuration.merge(my_configuration)
estimator = Estimator(run_configuration, save_estimation_results=False)
estimator.estimate()
#estimator.reestimate("randstad.estimation.HLCM_specification")
#estimator.reestimate("randstad.estimation.ELCM_specification", type="home_based")
    