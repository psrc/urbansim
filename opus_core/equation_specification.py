#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.resources import Resources
from opus_core.store.storage import Storage
from numpy import asarray, array, where, ndarray, ones, concatenate, maximum, resize, logical_and
from opus_core.misc import ematch
from opus_core.misc import unique_values
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
import sys

class EquationSpecification(object):
    # Names of attributes for specification data on storage
    field_submodel_id = 'sub_model_id'
    field_equation_id = 'equation_id'
    field_coefficient_name = 'coefficient_name'
    field_variable_name = 'variable_name'
    field_fixed_value = 'fixed_value'
    dim_field_prefix = 'dim_' # columns with this prefix are considered as additional dimensions of the specification

    def __init__(self, variables=None, coefficients=None, equations=None, submodels=None,
                 fixed_values=None, other_fields=None, specification_dict=None, in_storage=None, out_storage=None):
        """  variables - array of names of variables that are to be connected to coefficients.
            coefficients (coef. names), equations and submodels are arrays of the same length as variables or empty arrays.
            variables[i] is  meant to belong to coefficient[i], equations[i], submodels[i].
            fixed_values is an array with coeffcient values that should stay constant in the estimation. 
            other_fields should be a dictionary holding other columns of the specification table.
            The actual connection is done by SpecifiedCoefficients.
            If variables is None and specification_dict is not None, the specification is assume to be in one of the dictionary format,
            see doc string for get_specification_attributes_from_dictionary.
        """
        if (variables is None) and (specification_dict is not None):
            variables, coefficients, equations, submodels, fixed_values = get_specification_attributes_from_dictionary(specification_dict)
        self.variables = tuple(map(lambda x: VariableName(x), self._none_or_array_to_array(variables)))
        self.coefficients = self._none_or_array_to_array(coefficients)
        if not isinstance(self.coefficients, ndarray):
            self.coefficients=array(self.coefficients)
        self.equations = self._none_or_array_to_array(equations)
        if not isinstance(self.equations, ndarray):
            self.equations=array(self.equations)
        self.submodels=self._none_or_array_to_array(submodels)
        if not isinstance(self.submodels, ndarray):
            self.submodels=array(self.submodels)
        self.in_storage=in_storage
        self.out_storage=out_storage
        self.fixed_values=self._none_or_array_to_array(fixed_values)
        if not isinstance(self.fixed_values, ndarray):
            self.fixed_values=array(self.fixed_values)
        if other_fields:
            self.other_fields = other_fields
        else:
            self.other_fields = {}
        self.other_dim_field_names = []
        self.set_other_dim_field_names()

    def _none_or_array_to_array(self, array_or_none):
        if array_or_none is None:
            result = array([])
        else:
            result = array_or_none
        return result


    def load(self, resources=None, in_storage=None, in_table_name=None, variables = []):
        local_resources = Resources(resources)
        local_resources.merge_with_defaults({
            "field_submodel_id":self.field_submodel_id,
            "field_equation_id":self.field_equation_id,
            "field_coefficient_name":self.field_coefficient_name,
            "field_variable_name":self.field_variable_name,
            "field_fixed_value":self.field_fixed_value})
        if in_storage <> None:
            self.in_storage = in_storage
        if not isinstance(self.in_storage, Storage):
            logger.log_warning("in_storage is not of type Storage. No EquationSpecification loaded.")
        else:
            data = self.in_storage.load_table(table_name=in_table_name)
            equations=array([-1])
            if local_resources["field_equation_id"] in data:
                equations = data[local_resources["field_equation_id"]]
            vars=data[local_resources["field_variable_name"]]
            self.variables=tuple(map(lambda x: VariableName(x), vars))
            self.coefficients=data[local_resources["field_coefficient_name"]]
            if local_resources["field_submodel_id"] in data:
                submodels = data[local_resources["field_submodel_id"]]
            else:
                submodels = array([-2]*self.coefficients.size, dtype="int32")
            self.submodels=submodels
            if equations.max() >= 0:
                 self.equations=equations
            if local_resources["field_fixed_value"] in data:
                self.fixed_values = data[local_resources["field_fixed_value"]]
            for field in data:
                if field not in [local_resources["field_submodel_id"], local_resources["field_equation_id"],
                                 local_resources["field_variable_name"], local_resources["field_coefficient_name"],
                                 local_resources["field_fixed_value"]]:
                    self.other_fields[field] = data[field]
            if variables:
                self.shrink(variables)

    def write(self, resources=None, out_storage=None, out_table_name=None):
        """
        """ # TODO: insert docstring
        local_resources = Resources(resources)
        local_resources.merge_with_defaults({
            "field_submodel_id":self.field_submodel_id,
            "field_equation_id":self.field_equation_id,
            "field_coefficient_name":self.field_coefficient_name,
            "field_variable_name":self.field_variable_name,
            "field_fixed_value":self.field_fixed_value,
            "out_table_name":out_table_name})
        if out_storage <> None:
            self.out_storage = out_storage
        if not isinstance(self.out_storage, Storage):
            logger.log_warning("out_storage has to be of type Storage. No EquationSpecifications written.")
            return

        submodel_ids = self.get_submodels()
        if submodel_ids.size == 0:
            submodel_ids = resize(array([-2], dtype="int32"), len(self.get_coefficient_names())) #set sub_model_id = -2 when there is no or 1 submodels

        equation_ids = self.get_equations()
        if equation_ids.size == 0:
            equation_ids = resize(array([-2], dtype="int32"), submodel_ids.size)

        values = {local_resources["field_submodel_id"]: submodel_ids,
               local_resources["field_equation_id"]:  equation_ids,
               local_resources["field_coefficient_name"]:  self.get_coefficient_names(),
               local_resources["field_variable_name"]:  self.get_long_variable_names()}
        if self.fixed_values.size > 0:
            values[local_resources["field_fixed_value"]] = self.fixed_values
        for field in self.other_fields.keys():
            values[field] = self.other_fields[field]

        types = {local_resources["field_submodel_id"]: 'integer',
               local_resources["field_equation_id"]:  'integer',
               local_resources["field_coefficient_name"]:  'text',
               local_resources["field_variable_name"]:  'text'}

        local_resources.merge({"values":values, 'valuetypes': types, "drop_table_flag":1})
        
        self.out_storage.write_table(table_name = local_resources['out_table_name'],
            table_data=local_resources['values']
            )

    def shrink(self, variables):
        """ Shrink all arrays of class attributes to those elements that correspond to given variables.
        """
        variables = tuple(variables)
        idx_list = []
        variable_names = asarray(map(lambda x: x.get_alias(),
                                                  self.variables))
        for var in variables:
            idx = ematch(variable_names, var)
            if idx.size > 0:
                idx_list.append(idx[0])
        idx_array = asarray(idx_list)
        self.variables = tuple(map(lambda x: VariableName(x), variable_names[idx_array]))
        self.coefficients = self.coefficients[idx_array]
        if self.submodels.size > 0:
            self.submodels = self.submodels[idx_array]
        if self.equations.size > 0:
            self.equations = self.equations[idx_array]
        if self.fixed_values.size > 0:
            self.fixed_values = self.fixed_values[idx_array]
        for field in self.other_fields.keys():
            self.other_fields[field] = self.other_fields[field][idx_array]

    def add_item(self, variable_name, coefficient_name, submodel=None, equation=None, fixed_value=None, other_fields=None):
        if isinstance(variable_name,VariableName):
            self.variables = self.variables + (variable_name,)
        else:
            self.variables = self.variables + (VariableName(variable_name),)
        self.coefficients = concatenate((self.coefficients, array([coefficient_name])))
        if submodel is not None:
            self.submodels = concatenate((self.submodels, array([submodel], dtype=self.submodels.dtype)))
        if equation is not None:
            self.equations = concatenate((self.equations, array([equation], dtype=self.equations.dtype)))
        if fixed_value is not None:
            self.fixed_values = concatenate((self.fixed_values, array([fixed_value], dtype=self.fixed_values.dtype)))
        if other_fields is not None:
            for field in other_fields.keys():
                self.other_fields[field] = concatenate((self.other_fields[field], array([other_fields[field]],
                                                                               dtype=self.other_fields[field].dtype)))

    def summary(self):
        logger.log_status("Specification object:")
        logger.log_status("size:", len(self.variables))
        logger.log_status("variables:")
        logger.log_status(map(lambda x: x.get_alias(), self.variables))
        logger.log_status("coefficients:")
        logger.log_status(self.coefficients)
        if self.equations.size > 0:
            logger.log_status("equations:")
            logger.log_status(self.equations)
        if self.submodels.size > 0:
            logger.log_status("submodels:")
            logger.log_status(self.submodels)
        if self.fixed_values.size > 0:
            logger.log_status("fixed_values:")
            logger.log_status(self.fixed_values)    
        for field in self.other_fields.keys():
            logger.log_status("%s:" % field)
            logger.log_status(self.other_fields[field])

    def compare_and_try_raise_speclengthexception(self, value, compvalue, name):
        if value != compvalue:
            try:
                raise SpecLengthException(name)
            except SpecLengthException, msg:
                logger.log_status(msg)
                sys.exit(1)


    def check_consistency(self):
        self.compare_and_try_raise_speclengthexception(len(self.variables),self.coefficients.size,"coefficients")
        if self.equations.size > 0:
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.equations.size,"equations")
        if self.submodels.size > 0:
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.submodels.size,"submodels")
        for field in self.other_fields.keys():
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.other_fields[field].size, field)

    def get_variable_names(self):
        return array(map(lambda x: x.get_alias(), self.variables))

    def get_long_variable_names(self):
        return array(map(lambda x: x.get_expression(), self.variables))

    def get_variables(self):
        return self.variables

    def get_coefficient_names(self):
        return self.coefficients

    def get_distinct_coefficient_names(self):
        return unique_values(self.coefficients)

    def get_distinct_variable_names(self):
        return unique_values(self.get_variable_names())

    def get_distinct_long_variable_names(self):
        return unique_values(self.get_long_variable_names())

    def get_equations(self):
        return self.equations

    def get_submodels(self):
        return self.submodels

    def get_fixed_values(self):
        return self.fixed_values

    def get_coefficient_fixed_values_for_submodel(self, submodel):
        """Return a tuple with two arrays: first one is an array of coefficient names that have fixed values (i.e. <> 0).
        The second array are the corresponding fixed values. The fixed values are considered for given submodel."""
        fixed_values = self.get_fixed_values()
        if fixed_values.size == 0:
            return (array([]), array([]))
        if self.get_submodels().size > 0:
            idx = self.get_submodels() == submodel
        else: 
            idx = ones(fixed_values.size, dtype="bool8")
        idx = logical_and(idx, fixed_values <> 0)
        return (self.get_coefficient_names()[idx], fixed_values[idx])
        
        
    def get_nequations(self):
        if self.get_equations().size > 0:
            return unique_values(self.get_equations()).size
        return 1

    def get_number_of_distinct_variables(self):
        return self.get_distinct_variable_names().size

    def get_distinct_submodels(self):
        return unique_values(self.get_submodels())

    def get_nsubmodels(self):
        return maximum(1, self.get_distinct_submodels().size)

    def get_other_field_names(self):
        return self.other_fields.keys()
        
    def get_other_dim_field_names(self):
        return self.other_dim_field_names
        
    def get_other_field(self, name):
        return self.other_fields[name]
        
    def get_distinct_values_of_other_field(self, name):
        values = self.get_other_field(name)
        return unique_values(values)
        
    def set_variable_prefix(self, prefix):
        self.variables = tuple(map(lambda name: VariableName(prefix + name),
                                     self.get_variable_names()))

    def set_dataset_name_of_variables(self, dataset_name):
        self.set_variable_prefix(dataset_name+".")

    def set_other_dim_field_names(self):
        """ Choose those names whose prefix correspond to self.dim_field_prefix."""
        for field in self.other_fields.keys():
            if field[0:len(self.dim_field_prefix)] == self.dim_field_prefix:
                self.other_dim_field_names.append(field)
                
    def get_indices_for_submodel(self, submodel):
        submodels = self.get_submodels()
        return where(submodels==submodel)[0]

    def get_equations_for_submodel(self, submodel):
        idx = self.get_indices_for_submodel(submodel)
        return unique_values(self.get_equations()[idx])

    def get_table_summary(self, submodel_default=-2, equation_default=-2):
        first_row = ['Submodel', 'Equation', 'Coefficient Name', 'Variable']
        submodels = self.get_submodels()
        variables = self.get_long_variable_names()
        coefficient_names = self.get_coefficient_names()
        equations = self.get_equations()
        if equations.size == 0:
            equations = equation_default * ones(variables.size, dtype="int32")
        if submodels.size == 0:
            submodels = submodel_default * ones(variables.size, dtype="int32")

        table = [first_row]
        for i in range(variables.size):
            table += [[submodels[i], equations[i], coefficient_names[i], variables[i]]]

        return table

    def replace_variables(self, new_variables):
        """new_variables is a dictionary with variable aliases as keys and new expressions as values.
        The methos replaces all variables where the alias matches with the new ones. 
        """
        current_aliases = self.get_variable_names()
        variables = list(self.get_variables())
        for alias, new_expr in new_variables.iteritems():
            idx = where(current_aliases == alias)[0]
            for i in range(idx.size):
                variables[idx[i]] = VariableName(new_expr)
        self.variables = tuple(variables)
        
#Functions
class SpecLengthException(Exception):
    def __init__(self, name):
        self.args = "Something is wrong with the size of the specification object " + name + "!"
        
def get_specification_attributes_from_dictionary(specification_dict):
    """ Creates a specification object from a dictionary specification_dict. Keys of the dictionary are submodels. If there
    is only one submodel, use -2 as key. A value of specification_dict for each submodel entry is a list containing specification for the particular submodel.
    The elements of each list can be defined in one of the following forms:
        - a character string specifying a variable in its fully qualified name or as an expression - in such a case 
                                the coeficient name will be the alias of the variable
        - a tuple of length 2: variable name as above, and the corresponding coefficient name
        - a tuple of length 3: variable name, coefficient name, fixed value of the coefficient (if the 
                                coefficient should not be estimated)
        - a dictionary with pairs variable name, coefficient name
    specification_dict can contain an entry '_definition_' which should be a list of elements in one of the forms above.
    In such a case, the entries defined for submodels can contain only the variable aliases. The corresponding 
    coefficient names and fixed values (if defined) are taken from the definition section. 
    See examples in unit tests below.
    """
    variables = []
    coefficients = []
    equations = []
    submodels = []
    fixed_values = []
    definition = {}
    try:
        if "_definition_" in specification_dict.keys():
            definition["variables"], definition["coefficients"], definition["equations"], dummy, definition["fixed_values"] = \
                            get_variables_coefficients_equations_for_submodel(specification_dict["_definition_"], "_definition_")
            definition["alias"]  = map(lambda x: VariableName(x).get_alias(), definition["variables"])
            del specification_dict["_definition_"]
        for sub_model, submodel_spec in specification_dict.items():
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
    return (array(variables), array(coefficients), array(equations, dtype="int16"), array(submodels, dtype="int16"), array(fixed_values))

def load_specification_from_dictionary(specification_dict):
    """See the doc string at get_specification_attributes_from_dictionary
    """
    variables, coefficients, equations, submodels, fixed_values = get_specification_attributes_from_dictionary(specification_dict)
    return EquationSpecification(variables=variables, coefficients=coefficients, equations = equations, submodels = submodels, fixed_values = fixed_values)

def get_variables_coefficients_equations_for_submodel(submodel_spec, sub_model, definition={}):
    variables = []
    coefficients = []
    equations = []
    submodels = []
    fixed_values = []
    if isinstance(submodel_spec, tuple) or isinstance(submodel_spec, list):
        variable, coefficient, fixed_value, error = get_variables_coefficients_equations_for_submodel_part(
                                                                         submodel_spec, definition)
        if error:
            logger.log_error("Error in specification of submodel %s." % sub_model)
        variables += variable
        coefficients += coefficient
        fixed_values += fixed_value
        submodels += len(variable)*[sub_model]
    elif isinstance(submodel_spec, dict):
        speckeys = submodel_spec.keys()
        if sum(map(lambda(x): isinstance(x, int), speckeys)) == len(speckeys): # keys are the equations
            for eq, spec in submodel_spec.iteritems():
                variable, coefficient, fixed_value, error = get_variables_coefficients_equations_for_submodel_part(
                                                                         spec, definition)
                if error:
                    logger.log_error("Error in specification of submodel %s equation %s" % (sub_model, eq))
                variables += variable
                coefficients += coefficient
                fixed_values += fixed_value
                submodels += len(variable)*[sub_model]
                equations += len(variable)*[eq]
        else:
            if submodel_spec.has_key("equation_ids"):
                equation_ids = submodel_spec["equation_ids"]
                del submodel_spec["equation_ids"]
            else:
                equation_ids = None
            
            for var, coef in submodel_spec.items():
                if not equation_ids:
                    if ("variables" in definition.keys()) and (var in definition["alias"]):
                        i = definition["alias"].index(var)
                        variables.append(definition["variables"][i])
                        coefficients.append(definition["coefficients"][i])
                        fixed_values.append(definition["fixed_values"][i])
                    else:
                        variables.append(var)
                        coefficients.append(coef)
                        fixed_values.append(0)
                    submodels.append(sub_model)
                elif type(coef) is list or type(coef) is tuple:
                    for i in range(len(coef)):
                        if coef[i] != 0:
                            if ("variables" in definition.keys()) and (var in definition["alias"]):
                                j = definition["alias"].index(var)
                                variables.append(definition["variables"][j])
                                fixed_values.append(definition["fixed_values"][j])
                            else:
                                variables.append(var)
                                fixed_values.append(0)
                            coefficients.append(coef[i])
                            equations.append(equation_ids[i])
                            submodels.append(sub_model)
                            
                else:
                    logger.log_error("Wrong specification format for submodel %s variable %s; \nwith equation_ids provided, coefficients must be a list or tuple of the same length of equation_ids" % sub_model, var)

    return (variables, coefficients, equations, submodels, fixed_values)

def get_variables_coefficients_equations_for_submodel_part(submodel_spec, definition={}):
    variables = []
    coefficients = []
    equations = []
    submodels = []
    fixed_values = []
    error = False
    for var_coef in submodel_spec:
        if isinstance(var_coef, str):
            #var_coef is just variables long names or alias
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
                logger.log_error("Wrong specification format for variable %s" % submodel_spec)
                error = True
        elif isinstance(var_coef, dict):
            variables.append(var_coef.keys()[0])
            coefficients.append(var_coef.values()[0])
            fixed_values.append(0)
        else:
            logger.log_error("Wrong specification format for variable %s" % submodel_spec)
            error = True
        
    return (variables, coefficients, fixed_values, error)

from numpy import alltrue, ma
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    def test_write_method_for_expressions(self):

        variables = ("x = y.disaggregate(mydataset.my_variable, intermediates=[myfaz])",
                     "z = y.disaggregate(mydataset.my_variable, intermediates=[myfaz, myzone])")
        coefficients = ('c1', 'c2')
        storage = StorageFactory().get_storage('dict_storage')
        specification = EquationSpecification(variables, coefficients)
        specification.write(out_storage=storage, out_table_name="spec")
        result = storage.load_table(table_name="spec")
        self.assert_(result['variable_name'][0] == variables[0], 'Error in equation_specification')
        self.assert_(result['variable_name'][1] == variables[1], 'Error in equation_specification')

    def test_load_write_specification(self):
        in_storage = StorageFactory().get_storage('dict_storage')
        out_storage = StorageFactory().get_storage('dict_storage')
        spec_data = {
             "variable_name": array(["var1", "var2", "var1"]),
             "coefficient_name": array(["coef1", "coef2", "coef1"]),
             "nest": array([1,1,2]),
             "fixed_value": array([0, 1, 0])
                     }
        in_storage.write_table(table_name='my_specification', table_data=spec_data)
        specification = EquationSpecification(in_storage=in_storage, out_storage=out_storage)
        specification.load(in_table_name='my_specification')
        specification.write(out_table_name="out_specification")
        result = out_storage.load_table("out_specification", column_names=["nest", "sub_model_id", "fixed_value"])
        self.assert_(alltrue(result['nest'] == spec_data["nest"]), 'Error in equation_specification')
        self.assert_(alltrue(result['fixed_value'] == spec_data["fixed_value"]), 'Error in equation_specification')
        self.assert_(alltrue(result['sub_model_id'] == array([-2, -2, -2], dtype="int32")),
                     'Error in equation_specification')
        
    def test_replace_variables(self):
        variables = ("x = y.disaggregate(mydataset.my_variable, intermediates=[myfaz])",
                     "z = y.disaggregate(mydataset.my_variable, intermediates=[myfaz, myzone])",
                     "y = y.some_variable")
        coefficients = ('c1', 'c2', 'c3')
        specification = EquationSpecification(variables, coefficients)
        new_variables = {'z': 'xxx.my_new_variable', 'q': 'xxx.variable_not_to_be_replaced', 'y': 'y.replaces_y'}
        specification.replace_variables(new_variables)
        result = specification.get_long_variable_names()
        self.assert_(alltrue(result == array([variables[0], 'xxx.my_new_variable', 'y.replaces_y'])),
                     "Error in replace_varibles")
        
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
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        fixedval = result.get_fixed_values()
        self.assert_(alltrue(coefs == array(["BPOP", "BINC", "BART", "BHWY", "BAGE"])),
                     msg = "Error in test_load_specification (coefficients)")
        self.assert_(alltrue(vars ==
                                 array(["population", "average_income", "is_near_arterial", "is_near_highway", "lage"])),
                     msg = "Error in test_load_specification (variables)")
        self.assert_(ma.allequal(subm, array([1, 1, 2, 2, 3])),
                     msg = "Error in test_load_specification (submodels)")
        self.assert_(fixedval.size == 0, msg = "Error in test_load_specification (fixed_values should be empty)")
        
        # add a variable with a fixed value coefficient
        specification[3].append(("constant", "C", 1))
        result = load_specification_from_dictionary(specification)
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
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        fixedval = result.get_fixed_values()
        self.assert_(alltrue(coefs == array(["BPOP", "BINC", "BAGE", "BART", "C", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition (coefficients)")
        self.assert_(alltrue(vars ==
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
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        subm = result.get_submodels()
        self.assert_(alltrue(coefs == array(["population", "average_income", "lage", "is_near_arterial", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (coefficients)")
        self.assert_(alltrue(vars ==
                                 array(["population", "average_income", "lage", "is_near_arterial", "is_near_highway"])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (variables)")
        self.assert_(ma.allequal(subm, array([1, 1, 1, 2, 2])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (submodels)")
        # test data type
        self.assert_(subm.dtype.name == "int16",
                     msg = "Error in data type of submodels.")
        
    def test_load_specification_with_definition_with_equations(self):
        specification = {
             "_definition_": [
                 "pop = urbansim.gridcell.population",
                 "inc = urbansim.gridcell.average_income",
                 "art = urbansim.gridcell.is_near_arterial",
                 ],
              -2: {
                "equation_ids": (1,2),
                 "pop": ("bpop",0), 
                 "inc": (0, "binc"), 
                 "art": ("bart", 0), 
                 "constant": ("asc", 0)
                             }
              }
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        eqs = result.get_equations()
        lvars = result.get_long_variable_names()
        self.assert_(alltrue(coefs == array(["asc", "bart", "bpop", "binc"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (coefficients)")
        self.assert_(alltrue(vars == array(["constant",  "art", "pop", "inc"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (variables)")
        self.assert_(ma.allequal(eqs, array([1,1,1,2])),
                     msg = "Error in test_load_specification_with_definition_with_equations (equations)")
        self.assert_(alltrue(lvars == array(["constant",  
                                             "art = urbansim.gridcell.is_near_arterial", 
                                            "pop = urbansim.gridcell.population", 
                                            "inc = urbansim.gridcell.average_income"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (long names of variables)")
        
    def test_load_specification_with_definition_with_equations_v2(self):
        specification = {
             "_definition_": [
                 ("pop = urbansim.gridcell.population", "bpop"),
                 "inc = urbansim.gridcell.average_income",
                 "art = urbansim.gridcell.is_near_arterial",
                 ],
              -2: {
                   1: [
                     "pop", 
                     "inc", 
                     "constant" ],
                    2: [ "art"]
                             }
              }
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        eqs = result.get_equations()
        lvars = result.get_long_variable_names()
        self.assert_(alltrue(coefs == array(["bpop", "inc", "constant", "art",])),
                     msg = "Error in test_load_specification_with_definition_with_equations_v2 (coefficients)")
        self.assert_(alltrue(vars == array(["pop", "inc", "constant",  "art"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (variables)")
        self.assert_(ma.allequal(eqs, array([1,1,1,2])),
                     msg = "Error in test_load_specification_with_definition_with_equations (equations)")
        self.assert_(alltrue(lvars == array(["pop = urbansim.gridcell.population", 
                                             "inc = urbansim.gridcell.average_income",
                                             "constant",  
                                             "art = urbansim.gridcell.is_near_arterial", 
                                            ])),
                     msg = "Error in test_load_specification_with_definition_with_equations (long names of variables)")


if __name__=='__main__':
    opus_unittest.main()

