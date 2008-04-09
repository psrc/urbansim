#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

# This file copied from psrc_parcel/estimation/run_estimation.py and adapated for
# running an estimation from the GUI.  Both this version and the original are in
# extreme need of a cleanup!

from urbansim.estimation.estimator import Estimator
from urbansim.estimation.estimator import plot_utility_diagnose
from urbansim.estimation.estimator import plot_correlation_diagnose
from psrc_parcel.configs.baseline import Baseline

# todo:  
# pass baseline as a param
# replace spec_file with a configuration & pass it in
# DONE pass in estimation config (look for execs)
# DONE rewrite update_controller_by_specification_from_module to take a config instead of a module name
# DONE write replacement for conf.get_updated_configuration_from_module method 

# revise model_system for import replacement

# need to get both urbansim_parcel and psrc_parcel versions of spec according to the stuff below:

# also pass spec_file

class EstimationRunner(object):

    def run_estimation(self, estimation_config, model, specification, save_estimation_results=True, diagnose=False):
        # added specification arg
        self.model = model
        # REMOVE self.spec_file = "%s_specification" % model[0].lower()
        ### TODO: Re-write this
        type = None
        add_member_prefix = False
        baseline_config = Baseline()
        if len(model) > 2:
            type = model[2]
            if len(model) > 3:
                add_member_prefix = model[3]
        if type is None:
            exec("from urbansim_parcel.estimation.%s_estimation_config import run_configuration" % model[0].lower())
            run_configuration["models_configuration"][self.model[1]]["controller"].replace(baseline_config["models_configuration"][self.model[1]]["controller"])
            run_configuration = update_controller_by_specification(
                                run_configuration, model[1],
                                specification)
        else:
            exec("from urbansim_parcel.estimation.%s_estimation_config import %s_configuration as config" % (model[0].lower(),
                  model[0].lower()))
            conf = config(type, add_member_prefix)
            run_configuration = conf.get_configuration()
            run_configuration["models_configuration"][conf.model_name]["controller"].replace(
                                                                 baseline_config["models_configuration"][conf.model_name]["controller"])
            run_configuration = conf.get_updated_configuration_from_module(
                                     run_configuration, "psrc_parcel.estimation.%s" % self.spec_file)

        if diagnose and self.model[0] != 'REPM':  #only works for LCM and derivatives
            model_name = model[1]
            #if type is not None:
                #model_name = "%s_%s" % (type, model_name)    
            procedure_name = run_configuration["models_configuration"][model_name]["controller"]["estimate"]["arguments"].get('procedure',
                                                                                                            "'opus_core.bhhh_mnl_estimation'")
            run_configuration["models_configuration"][model_name]["controller"]["estimate"]["arguments"]["procedure"]= "'%s_with_diagnose'" % \
                procedure_name[1:(len(procedure_name)-1)]

        run_configuration.replace(estimation_config)
        self.estimator = Estimator(run_configuration, save_estimation_results=save_estimation_results)
        self.estimator.estimate()


# adapted from update_controller_by_specification_from_module in urbansim.estimation.estimator
def update_controller_by_specification(run_configuration, model_name, specification):
    controller = run_configuration["models_configuration"][model_name]["controller"]
    # The following line was formerly:
    #     controller["import"][specification_module] = "specification as spec"
    # In urbansim.model_coordinators.model_system we add some additional code
    # to accomodate the 'gui_import_replacements' section.
    # This should result in the same bindings for variables as the old version.
    if "gui_import_replacements" not in controller:
        controller["gui_import_replacements"] = {}
    controller["gui_import_replacements"][model_name] = ["spec", specification]
    controller["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec"
    controller["prepare_for_estimate"]["arguments"]["specification_storage"] = "None"
    run_configuration["models_configuration"][model_name]["controller"].merge(controller)
    return run_configuration
