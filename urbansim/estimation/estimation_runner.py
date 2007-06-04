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

from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import update_controller_by_specification_from_module


class EstimationRunner(Estimator):

    models = {
        "hlcm": ("HLCM", "household_location_choice_model"),
        "elcm-industrial": ("ELCM", "employment_location_choice_model", "industrial", False), # uses general ELCM and therefore type will not
                                                                                              # be added to the model name
        "elcm-commercial": ("ELCM", "employment_location_choice_model", "commercial", False),
        "elcm-home_based": ("ELCM", "employment_location_choice_model", "home_based", True), 
        "dplcm-industrial": ("DPLCM", "development_location_choice_model", "industrial"),
        "dplcm-commercial": ("DPLCM", "development_location_choice_model", "commercial"),
        "dplcm-residential": ("DPLCM", "development_location_choice_model", "residential"),
        "lpm": ("LPM", "land_price_model"),
        "rlsm": ("RLSM", "residential_land_share_model")
        }
     
    def __init__(self, model, specification_from_module=False, package="urbansim", 
                  configuration={}, save_estimation_results=False, models=None):
        """
        'specification_from_module' is True if the specification is defined in a module rather than in a database.
        'package' determines in what package the user-defined specification module of the model lives. 
        It must be in the directory 'estimation' under the package.
        'configuration' is a dictionary with which the estimation configuration is updated, therefore it should
        contain user-specific settings.
        """
        if models is not None:
            self.models = models
    
        model_tuple = self.models[model]
        type = None
        add_member_prefix = None
        if len(model_tuple) > 2:
            type = model_tuple[2]
            if len(model_tuple) > 3:
                add_member_prefix = model_tuple[3]
        if type is None:
            exec("from urbansim.configs.%s_estimation_config import run_configuration as config" % model_tuple[0].lower())
            run_configuration = config.copy()
            if specification_from_module:
                run_configuration = update_controller_by_specification_from_module(
                                run_configuration, model_tuple[1],
                                "%s.estimation.%s_specification" % (package, model_tuple[0]))
        elif add_member_prefix is not None:
            exec("from urbansim.configs.%s_estimation_config import %s_configuration as config" % ( 
                          model_tuple[0].lower(), model_tuple[0].lower()))        
            conf = config(type, add_member_prefix)
            run_configuration = conf.get_configuration()
            if specification_from_module:
                run_configuration = conf.get_updated_configuration_from_module(run_configuration, specification_module="%s.estimation.%s_specification" % (
                            package, model_tuple[0]))
            #run_configuration = conf.get_updated_configuration_from_module(run_configuration)
        else:  #necessary for developer model estimation
            exec("from urbansim.configs.%s_estimation_config import %s_configuration as config" % ( 
                          model_tuple[0].lower(), model_tuple[0].lower()))        
            conf = config(type)
            run_configuration = conf.get_configuration()
            if specification_from_module:
                run_configuration = conf.get_updated_configuration_from_module(run_configuration, specification_module="%s.estimation.%s_specification" % (
                            package, model_tuple[0]))
            
        run_configuration.merge(configuration)
        Estimator.__init__(self, run_configuration, save_estimation_results=save_estimation_results)

    