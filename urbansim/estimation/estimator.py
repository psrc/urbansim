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

from numpy import absolute, array, where
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.coefficients import Coefficients
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.misc import load_table_from_text_file
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset import Dataset
from opus_core.equation_specification import EquationSpecification
from opus_core.storage_factory import StorageFactory
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.session_configuration import SessionConfiguration

from urbansim.model_coordinators.model_system import ModelSystem

class Estimator(object):
    def __init__(self, config=None, save_estimation_results=False):
        if 'cache_directory' not in config or config['cache_directory'] is None:
            raise KeyError("The cache directory must be specified in the "
                "given configuration, giving the filesystem path to the cache "
                "directory containing the data with which to estimate. Please "
                "check that your configuration contains the 'cache_directory' "
                "entry and that it is not None.")

        self.simulation_state = SimulationState(new_instance=True)
        self.simulation_state.set_cache_directory(config['cache_directory'])

        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,
                             package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions,
                             in_storage=AttributeCache())
        self.config = Resources(config)
        self.save_estimation_results = save_estimation_results
        self.debuglevel = self.config.get("debuglevel", 4)
        self.model_system = ModelSystem()

        models = self.config.get('models',[])

        self.model_name = None
        if "model_name" in config.keys():
            self.model_name = config["model_name"]
        else:
            for model in models:
                if isinstance(model, dict):
                    model_name = model.keys()[0]
                    if (model[model_name] == "estimate") or (isinstance(model[model_name], list)
                        and ("estimate" in model[model_name])):
                            self.model_name = model_name
                            break

    def estimate(self, out_storage=None):
        self.model_system.run(self.config, write_datasets_to_cache_at_end_of_year=False)
        self.extract_coefficients_and_specification()

        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)

    def reestimate(self, specification_module_name, out_storage=None, type=None, submodels=None):
        """specification_module_name is name of a module that contains a dictionary called
        'specification'. 'type' is the name of model member, such as 'commercial', 'residential'. The specification dictionary
        is expected to have an entry of this name. If 'submodels' is given (list or a number),
        the restimation is done only for those submodels.
        """
        exec("import " + specification_module_name)
        eval("reload (" + specification_module_name + ")")
        exec("specification_dict =" + specification_module_name + ".specification")
        if type is not None:
            specification_dict = specification_dict[type]
        if submodels is not None: #remove all submodels but the given ones from specification
            submodels_to_be_deleted = specification_dict.keys()
            if not isinstance(submodels, list):
                submodels = [submodels]
            for sm in submodels:
                if sm not in submodels_to_be_deleted:
                    raise ValueError, "Submodel %s not in the specification." % sm
                submodels_to_be_deleted.remove(sm)
                if "_definition_" in submodels_to_be_deleted:
                    submodels_to_be_deleted.remove("_definition_")
            for sm in submodels_to_be_deleted:
                del specification_dict[sm]
        specification = load_specification_from_variable(specification_dict)
        new_namespace = self.model_system.run_year_namespace
        new_namespace["specification"] = specification
        self.model_system.do_process(new_namespace)
        self.extract_coefficients_and_specification()
        if self.save_estimation_results:
            self.save_results(out_storage=out_storage)

    def save_results(self, out_storage=None, model_name=None):
        if self.specification is None or self.coefficients is None:
            raise ValueError, "model specification or coefficient is None"

        #invalid = self.coefficients.is_invalid()
        if False:
            logger.log_warning('Invalid coefficients. Not saving results!')
            return

        if model_name is None:
            if self.model_name is not None:
                model_name = self.model_name
            else:
                raise ValueError, "model_name unspecified"

        if out_storage:
            pass
        elif 'output_configuration' in self.config:
            config = DatabaseServerConfiguration(
                host_name = self.config['output_configuration'].host_name,
                user_name = self.config['output_configuration'].user_name,
                password = self.config['output_configuration'].password
            )
            db_server = DatabaseServer(config)
            database_name = self.config["output_configuration"].database_name

            if not db_server.has_database(database_name):
                db_server.create_database(database_name)

            output_db = db_server.get_database(database_name,
                                               scenario=False)
            out_storage = StorageFactory().build_storage_for_dataset(type='sql_storage',
                storage_location=output_db)
        else:
            raise StandardError, "No output_configuration given."

        # the original model name of development_project_lcm is too long as a mysql db table name, truncate it
        if model_name.rfind("_development_project_location_choice_model") >=0:
            model_name = model_name.replace('_project', '')
        specification_table = '%s_specification' % model_name
        coefficients_table = '%s_coefficients' % model_name
        self.specification.write(out_storage=out_storage, out_table_name=specification_table)
        self.coefficients.write(out_storage=out_storage, out_table_name=coefficients_table)
        self.cache_specification_and_coefficients(out_storage, specification_table, coefficients_table)

    def cache_specification_and_coefficients(self, storage, specification_table, coefficients_table):
        for table_name in [specification_table, coefficients_table]:
            dataset = Dataset(in_storage=storage,
                          in_table_name=table_name,
                          id_name=[], debug = self.config.get("debuglevel",0))
            dataset.load_dataset()
            dataset.flush_dataset()

    def extract_coefficients_and_specification(self):
        for key in self.model_system.run_year_namespace.keys():
            if isinstance(self.model_system.run_year_namespace[key], Coefficients):
                self.coefficients = self.model_system.run_year_namespace[key]
            if isinstance(self.model_system.run_year_namespace[key], EquationSpecification):
                self.specification = self.model_system.run_year_namespace[key]
       #for key in self.model_system.vardict.keys():
#            if key.rfind("coefficients") >=0:
#                if isinstance(self.model_system.vardict[key], tuple):
#                    self.coefficients = self.model_system.vardict[key][0]
#                else:
#                    self.coefficients = self.model_system.vardict[key]
#            if key.rfind("specification") >=0:
#                if isinstance(self.model_system.vardict[key], tuple):
#                    self.specification = self.model_system.vardict[key][0]
#                else:
#                    self.specification = self.model_system.vardict[key]

    def get_data(self, coefficient, submodel=-2):
        return self.get_model().get_data(coefficient, submodel)

    def get_coefficient_names(self, submodel=-2):
        return self.get_model().get_coefficient_names(submodel)

    def get_data_as_dataset(self, submodel=-2):
        return self.get_model().get_data_as_dataset(submodel)

    def get_model(self):
        return self.model_system.run_year_namespace["model"]
        
    def get_choice_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_index(2)
        
    def get_agent_set_index(self): # works only for choice models
        return self.get_model().model_interaction.interaction_datasets[0].get_index(1)
        
    def cleanup(self, remove_cache=True):
        """Use this only if you don't want to reestimate."""
        self.simulation_state.remove_singleton(delete_cache=remove_cache)
        SessionConfiguration().remove_singleton()

def load_specification_from_variable(spec_var):
    """ Creates a specification object from a dictionary spec_var. Keys of the dictionary are submodels. If there
    is one submodel, use -2 as key. A values of spec_var is a list containing specification for the particular submodel.
    The elements of each list can be defined in one of the following forms:
        - a character string specifying a variable in its fully qualified name or as an expression - in such a case 
                                the coeficient name will be the alias of the variable
        - a tuple of length 2: variable name as above, and the corresponding coefficient name
        - a tuple of length 3: variable name, coefficient name, fixed value of the coefficient (here the 
                                coefficient won't be estimated)
        - a dictionary with pairs variable name, coefficient name
    spec_var can contain an entry '_definition_' which should be a list of elements in one of the forms above.
    In such a case, the entries defined for submodels can contain only the variable aliases. The corresponding 
    coefficient names and fixed values (if defined) are taken from the definition section. 
    For examples see unit test below.
    """
    variables = []
    coefficients = []
    equations = []
    submodels = []
    fixed_values = []
    definition = {}
    try:
        if "_definition_" in spec_var.keys():
            definition["variables"], definition["coefficients"], definition["equations"], dummy, definition["fixed_values"] = \
                            get_variables_coefficients_equations_for_submodel(spec_var["_definition_"], "_definition_")
            definition["alias"]  = map(lambda x: VariableName(x).get_alias(), definition["variables"])
            del spec_var["_definition_"]
        for sub_model, submodel_spec in spec_var.items():
            variable, coefficient, equation, submodel, fixed_value = get_variables_coefficients_equations_for_submodel(
                                                                         submodel_spec, sub_model, definition)
            variables += variable
            coefficients += coefficient
            equations += equation
            submodels += submodel
            fixed_values += fixed_value

    except Exception, e:
        logger.log_stack_trace()
        raise ValueError, "Wrong specification format for model specification: %s" % e

    if where(array(fixed_values) <> 0)[0].size == 0: # no fixed values defined
        fixed_values = []
    specification = EquationSpecification(variables=array(variables),
                                          coefficients=array(coefficients),
                                          equations = array(equations, dtype="int16"),
                                          submodels = array(submodels, dtype="int16"),
                                          fixed_values = array(fixed_values)
                                          )
    return specification

def get_variables_coefficients_equations_for_submodel(submodel_spec, sub_model, definition={}):
    variables = []
    coefficients = []
    equations = []
    submodels = []
    fixed_values = []
    if isinstance(submodel_spec, tuple) or isinstance(submodel_spec, list):
        for var_coef in submodel_spec:
            if isinstance(var_coef, str):
                #var_coef is actually just variables long names or alias
                if ("variables" in definition.keys()) and (var_coef in definition["alias"]):
                    i = definition["alias"].index(var_coef)
                    variables.append(definition["variables"][i])
                    coefficients.append(definition["coefficients"][i])
                    fixed_values.append(definition["fixed_values"][i])
                else:
                    variables.append(var_coef)
                    coefficients.append(VariableName(var_coef).get_alias())
                    fixed_values.append(0)
            elif isinstance(var_coef, tuple) or isinstance(var_coef, list):
                if len(var_coef) == 1: # coefficient name is created from variable alias
                    variables.append(var_coef[0])
                    coefficients.append(VariableName(var_coef[0]).get_alias())
                    fixed_values.append(0)
                elif len(var_coef) > 1: # coefficient names explicitely given
                    variables.append(var_coef[0])
                    coefficients.append(var_coef[1])
                    if len(var_coef) > 2: # third item is the coefficient fixed value 
                        fixed_values.append(var_coef[2])
                    else:
                        fixed_values.append(0)
                else:
                    logger.log_error("Wrong specification format for submodel %s variable %s" % sub_model, submodel_spec)
            elif isinstance(var_coef, dict):
                variables.append(var_coef.keys()[0])
                coefficients.append(var_coef.values()[0])
                fixed_values.append(0)
            else:
                logger.log_error("Wrong specification format for submodel %s variable %s" % sub_model, submodel_spec)
            submodels.append(sub_model)
    elif isinstance(submodel_spec, dict):
        if submodel_spec.has_key("equation_ids"):
            equation_ids = submodel_spec["equation_ids"]
            del submodel_spec["equation_ids"]
        else:
            equation_ids = None
        for var, coef in submodel_spec.items():
            if not equation_ids:
                variables.append(var)
                coefficients.append(coef)
                submodels.append(sub_model)
                fixed_values.append(0)
            elif type(coef) is list or type(coef) is tuple:
                for i in range(len(coef)):
                    if coef[i] != 0:
                        variables.append(var)
                        coefficients.append(coef[i])
                        equations.append(equation_ids[i])
                        submodels.append(sub_model)
                        fixed_values.append(0)
            else:
                logger.log_error("Wrong specification format for submodel %s variable %s; \nwith equation_ids provided, coefficients must be a list or tuple of the same length of equation_ids" % sub_model, var)

    return (variables, coefficients, equations, submodels, fixed_values)


def get_specification_for_estimation(specification_dict=None, specification_storage=None,
                                        specification_table = None):
    if specification_dict is not None:
        return load_specification_from_variable(specification_dict)
    from opus_core.choice_model import prepare_specification_and_coefficients
    (specification, dummy) = prepare_specification_and_coefficients(specification_storage, specification_table)
    return specification

def update_controller_by_specification_from_module(run_configuration, model_name, specification_module):
    controller = run_configuration["models_configuration"][model_name]["controller"]
    controller["import"][specification_module] = "specification as spec"
    controller["prepare_for_estimate"]["arguments"]["specification_dict"] = "spec"
    controller["prepare_for_estimate"]["arguments"]["specification_storage"] = "None"

    run_configuration["models_configuration"][model_name]["controller"].merge(controller)
    return run_configuration

def plot_utility_diagnose(filename):
    from opus_core.plot_functions import plot_barchart
    data, coef_names = load_table_from_text_file(filename, convert_to_float=True, header=True)
    plot_barchart(data[2,:], labels = coef_names)

def plot_correlation_diagnose(filename):
    from opus_core.plot_functions import plot_matplot
    data, coef_names = load_table_from_text_file(filename, convert_to_float=True, header=True)
    plot_matplot(absolute(data), xlabels = coef_names, ylabels=coef_names)


from opus_core.tests import opus_unittest
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def test_load_specification(self):
        specification = {1: [
                 ("urbansim.gridcell.population", "BPOP"),
                 ("urbansim.gridcell.average_income", "BINC"),
                             ],
                         2: [
                 ("urbansim.gridcell.is_near_arterial", "BART"),
                 ("urbansim.gridcell.is_near_highway", "BHWY"),
                             ],
                         3: [
                 ("lage = ln(urbansim.gridcell.average_age+1)", "BAGE")
                             ]
        }
        result = load_specification_from_variable(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        fixedval = result.get_fixed_values()
        self.assert_(ma.allequal(coefs, array(["BPOP", "BINC", "BART", "BHWY", "BAGE"])),
                     msg = "Error in test_load_specification (coefficients)")
        self.assert_(ma.allequal(vars,
                                 array(["population", "average_income", "is_near_arterial", "is_near_highway", "lage"])),
                     msg = "Error in test_load_specification (variables)")
        self.assert_(ma.allequal(subm, array([1, 1, 2, 2, 3])),
                     msg = "Error in test_load_specification (submodels)")
        self.assert_(fixedval.size == 0, msg = "Error in test_load_specification (fixed_values should be empty)")
        
        # add a variable with a fixed value coefficient
        specification[3].append(("constant", "C", 1))
        result = load_specification_from_variable(specification)
        fixedval = result.get_fixed_values()
        self.assert_(ma.allequal(fixedval, array([0, 0, 0, 0, 0, 1])), 
                     msg = "Error in test_load_specification (fixed_values)")
        
    def test_load_specification_with_definition(self):
        specification = {
             "_definition_": [
                 ("urbansim.gridcell.population", "BPOP"),
                 ("urbansim.gridcell.average_income", "BINC"),
                 ("urbansim.gridcell.is_near_arterial", "BART"),
                 ("lage = ln(urbansim.gridcell.average_age+1)", "BAGE"),
                 ("constant", "C", 1.5)
                 ],
              1: [
                 "population", "average_income", "lage"
                             ],
              2: [
                "is_near_arterial",
                "constant",
                 ("urbansim.gridcell.is_near_highway", "BHWY"),
                             ],
        }
        result = load_specification_from_variable(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        fixedval = result.get_fixed_values()
        self.assert_(ma.allequal(coefs, array(["BPOP", "BINC", "BAGE", "BART", "C", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition (coefficients)")
        self.assert_(ma.allequal(vars,
                                 array(["population", "average_income", "lage", "is_near_arterial", "constant", 
                                        "is_near_highway"])),
                     msg = "Error in test_load_specification_with_definition (variables)")
        self.assert_(ma.allequal(subm, array([1, 1, 1, 2, 2, 2])),
                     msg = "Error in test_load_specification_with_definition (submodels)")
        self.assert_(ma.allclose(fixedval, array([0, 0, 0, 0, 1.5, 0])), 
                     msg = "Error in test_load_specification_with_definition (fixed_values)")

    def test_load_specification_with_definition_with_implicit_coefficients(self):
        """Coeficient names should be aliases of the variables."""
        specification = {
             "_definition_": [
                 "urbansim.gridcell.population",
                 "urbansim.gridcell.average_income",
                 "urbansim.gridcell.is_near_arterial",
                 "lage = ln(urbansim.gridcell.average_age+1)",
                 ],
              1: [
                 "population", "average_income", "lage"
                             ],
              2: [
                "is_near_arterial",
                 ("urbansim.gridcell.is_near_highway", "BHWY"),
                             ],
        }
        result = load_specification_from_variable(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        self.assert_(ma.allequal(coefs, array(["population", "average_income", "lage", "is_near_arterial", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition (coefficients)")
        self.assert_(ma.allequal(vars,
                                 array(["population", "average_income", "lage", "is_near_arterial", "is_near_highway"])),
                     msg = "Error in test_load_specification_with_definition (variables)")
        self.assert_(ma.allequal(subm, array([1, 1, 1, 2, 2])),
                     msg = "Error in test_load_specification_with_definition (submodels)")
        # test data type
        self.assert_(subm.dtype.name == "int16",
                     msg = "Error in data type of submodels.")

if __name__=='__main__':
    opus_unittest.main()