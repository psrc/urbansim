# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.store.storage import Storage
from numpy import asarray, array, where, ndarray, ones, concatenate, maximum, resize, logical_and
from opus_core.misc import ematch, unique
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
            variables, coefficients, equations, submodels, fixed_values, other_fields = \
                                            get_specification_attributes_from_dictionary(specification_dict)
        self.variables = tuple([VariableName(x) for x in self._none_or_array_to_array(variables)])
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
        if in_storage != None:
            self.in_storage = in_storage
        if not isinstance(self.in_storage, Storage):
            logger.log_warning("in_storage is not of type Storage. No EquationSpecification loaded.")
        else:
            data = self.in_storage.load_table(table_name=in_table_name)
            equations=array([-1])
            if local_resources["field_equation_id"] in data:
                equations = data[local_resources["field_equation_id"]]
            vars=data[local_resources["field_variable_name"]]
            self.variables=tuple([VariableName(x) for x in vars])
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
            self.set_other_dim_field_names()
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
        if out_storage != None:
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
        for field in list(self.other_fields.keys()):
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
        variable_names = asarray([x.get_alias() for x in self.variables])
        for var in variables:
            idx = ematch(variable_names, var)
            if idx.size > 0:
                idx_list.append(idx[0])
        idx_array = asarray(idx_list)
        self.do_shrink(variable_names, idx_array)
        
    def do_shrink(self, variable_names, idx_array):
        new_variables = []
        for i in idx_array:
            new_variables.append(self.variables[i])
        self.variables = tuple(new_variables)
        tuple([VariableName(x) for x in variable_names[idx_array]])
        self.coefficients = self.coefficients[idx_array]
        if self.submodels.size > 0:
            self.submodels = self.submodels[idx_array]
        if self.equations.size > 0:
            self.equations = self.equations[idx_array]
        if self.fixed_values.size > 0:
            self.fixed_values = self.fixed_values[idx_array]
        for field in list(self.other_fields.keys()):
            self.other_fields[field] = self.other_fields[field][idx_array]
            
    def delete(self, variables):
        """ Delete given variables from specification."""
        variables = tuple(variables)
        idx_list = []
        variable_names = asarray([x.get_alias() for x in self.variables])
        nvariables = variable_names.size
        will_not_delete = array(nvariables*[True], dtype='bool8')
        for var in variables:
            idx = ematch(variable_names, var)
            if idx.size > 0:
                will_not_delete[idx] = False
        self.do_shrink(variable_names, where(will_not_delete)[0])

    def add_item(self, variable_name, coefficient_name, submodel=None, equation=None, fixed_value=None, other_fields=None):
        if isinstance(variable_name,VariableName):
            self.variables = self.variables + (variable_name,)
        else:
            self.variables = self.variables + (VariableName(variable_name),)
        self.coefficients = concatenate((self.coefficients, array([coefficient_name])))
        if submodel is not None and self.get_submodels().size > 0:
            self.submodels = concatenate((self.submodels, array([submodel], dtype=self.submodels.dtype)))
        elif self.get_submodels().size > 0:
            self.submodels = concatenate((self.submodels, array([-2], dtype=self.submodels.dtype)))
        if equation is not None and self.get_equations().size > 0:
            self.equations = concatenate((self.equations, array([equation], dtype=self.equations.dtype)))
        elif self.get_equations().size > 0:
            self.equations = concatenate((self.equations, array([-2], dtype=self.equations.dtype)))
        if fixed_value is not None and self.get_fixed_values().size > 0:
            self.fixed_values = concatenate((self.fixed_values, array([fixed_value], dtype=self.fixed_values.dtype)))
        elif self.get_fixed_values().size > 0:
            self.fixed_values = concatenate((self.fixed_values, array([0], dtype=self.fixed_values.dtype)))
        if other_fields is not None:
            for field in list(other_fields.keys()):
                self.other_fields[field] = concatenate((self.other_fields[field], array([other_fields[field]],
                                                                               dtype=self.other_fields[field].dtype)))

    def summary(self):
        logger.log_status("Specification object:")
        logger.log_status("size:", len(self.variables))
        logger.log_status("variables:")
        logger.log_status([x.get_alias() for x in self.variables])
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
        for field in list(self.other_fields.keys()):
            logger.log_status("%s:" % field)
            logger.log_status(self.other_fields[field])

    def compare_and_try_raise_speclengthexception(self, value, compvalue, name):
        if value != compvalue:
            #try:
            raise SpecLengthException(name)
            #except SpecLengthException, msg:
            #    logger.log_status(msg)
            #    sys.exit(1)


    def check_consistency(self):
        self.compare_and_try_raise_speclengthexception(len(self.variables),self.coefficients.size,"coefficients")
        if self.equations.size > 0:
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.equations.size,"equations")
        if self.submodels.size > 0:
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.submodels.size,"submodels")
        for field in list(self.other_fields.keys()):
            self.compare_and_try_raise_speclengthexception(len(self.variables),self.other_fields[field].size, field)

    def get_variable_names(self):
        return array([x.get_alias() for x in self.variables])

    def get_long_variable_names(self):
        return array([x.get_expression() for x in self.variables])

    def get_variables(self):
        return self.variables

    def get_coefficient_names(self):
        return self.coefficients

    def get_distinct_coefficient_names(self):
        return unique(self.coefficients)

    def get_distinct_variable_names(self):
        return unique(self.get_variable_names())

    def get_distinct_long_variable_names(self):
        return unique(self.get_long_variable_names())

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
        idx = logical_and(idx, fixed_values != 0)
        return (self.get_coefficient_names()[idx], fixed_values[idx])
        
        
    def get_nequations(self):
        if self.get_equations().size > 0:
            return unique(self.get_equations()).size
        return 1

    def get_number_of_distinct_variables(self):
        return self.get_distinct_variable_names().size

    def get_distinct_submodels(self):
        return unique(self.get_submodels())

    def get_nsubmodels(self):
        return maximum(1, self.get_distinct_submodels().size)

    def get_other_fields(self):
        return self.other_fields
    
    def get_other_field_names(self):
        return list(self.other_fields.keys())
        
    def get_other_dim_field_names(self):
        return self.other_dim_field_names
        
    def get_other_field(self, name):
        return self.other_fields[name]
        
    def get_distinct_values_of_other_field(self, name):
        values = self.get_other_field(name)
        return unique(values)
        
    def set_variable_prefix(self, prefix):
        self.variables = tuple([VariableName(prefix + name) for name in self.get_variable_names()])

    def set_dataset_name_of_variables(self, dataset_name):
        self.set_variable_prefix(dataset_name+".")

    def set_other_dim_field_names(self):
        """ Choose those names whose prefix correspond to self.dim_field_prefix."""
        for field in list(self.other_fields.keys()):
            if field[0:len(self.dim_field_prefix)] == self.dim_field_prefix:
                self.other_dim_field_names.append(field)
                
    def get_indices_for_submodel(self, submodel):
        submodels = self.get_submodels()
        return where(submodels==submodel)[0]

    def get_equations_for_submodel(self, submodel):
        idx = self.get_indices_for_submodel(submodel)
        return unique(self.get_equations()[idx])

    def get_table_summary(self, submodel_default=-2, equation_default=-2):
        submodels = self.get_submodels()
        variables = self.get_long_variable_names()
        coefficient_names = self.get_coefficient_names()
        equations = self.get_equations()
        if equations.size == 0:
            #equations = equation_default * ones(variables.size, dtype="int32")
            first_row = ['Submodel', 'Coefficient Name', 'Variable']
        else:
            first_row = ['Submodel', 'Equation', 'Coefficient Name', 'Variable']
        if submodels.size == 0:
            submodels = submodel_default * ones(variables.size, dtype="int32")

        table = [first_row]
        for i in range(variables.size):
            if equations.size == 0:
                table += [[submodels[i], coefficient_names[i], variables[i]]]
            else:
                table += [[submodels[i], equations[i], coefficient_names[i], variables[i]]]

        return table

    def replace_variables(self, new_variables):
        """new_variables is a dictionary with variable aliases as keys and new expressions as values.
        The methos replaces all variables where the alias matches with the new ones. 
        """
        current_aliases = self.get_variable_names()
        variables = list(self.get_variables())
        for alias, new_expr in new_variables.items():
            idx = where(current_aliases == alias)[0]
            for i in range(idx.size):
                variables[idx[i]] = VariableName(new_expr)
        self.variables = tuple(variables)
        
    def copy_equations_for_dim_if_needed(self, eqs_ids, dim_name, dim_value):
        """If there are equations equal -2 for the specified dim_name and value, it 
        is copied for each eqs_id.
        """
        idx = where(self.other_fields[dim_name] == dim_value)[0]
        if self.get_equations().size == 0:
            self.equations = array(len(self.variables)*[-2], dtype='int32')
 
        idx_to_copy = idx[where(self.get_equations()[idx] == -2)[0]]
        for i in idx_to_copy:
            for eq in eqs_ids:
                if eq == eqs_ids[0]: # first call
                    self.equations[i] = eq
                    continue
                other_fields={}
                for of_name, of_values in self.other_fields.items():
                    other_fields[of_name] = of_values[i]
                subm = None
                if self.get_submodels().size>0:
                    subm = self.get_submodels()[i]
                fv = None
                if self.get_fixed_values().size > 0:
                    fv = self.get_fixed_values()[i]
                self.add_item(self.get_long_variable_names()[i], coefficient_name=self.get_coefficient_names()[i], 
                          submodel=subm, equation=eq, fixed_value=fv, other_fields=other_fields)        
        
#Functions
class SpecLengthException(Exception):
    def __init__(self, name):
        self.value = "Something is wrong with the size of the specification object: %s." % name
    
    def __str__(self):
        return repr(self.value)
        
def get_specification_attributes_from_dictionary(specification_dict):
    """ Creates a specification object from a dictionary specification_dict. Keys of the dictionary are submodels. If there
    is only one submodel, use -2 as key. A value of specification_dict for each submodel entry is either a list 
    or a dictionary containing specification for the particular submodel.
    
    If it is a list, each element can be defined in one of the following forms:
        - a character string specifying a variable in its fully qualified name or as an expression - in such a case 
                                the coefficient name will be the alias of the variable
        - a tuple of length 2: variable name as above, and the corresponding coefficient name
        - a tuple of length 3: variable name, coefficient name, fixed value of the coefficient (if the 
                                coefficient should not be estimated)
        - a dictionary with pairs variable name, coefficient name
        
    If it is a dictionary, it can contain specification for each equation or for elements of other fields.
    It can contain an entry 'name' which specifies the name of the field (by default the name is 'equation').
    If it is another name, the values are stored in the dictionary attribute 'other_fields'. Each element of the 
    submodel dictionary can be again a list (see the previous paragraph), or a dictionary 
    (like the one described in this paragraph).
    
    specification_dict can contain an entry '_definition_' which should be a list of elements in one of the forms
    described in the second paragraph.
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
    other_fields = {}
    try:
        if "_definition_" in list(specification_dict.keys()):
            definition["variables"], definition["coefficients"], definition["equations"], dummy1, definition["fixed_values"], dummy2 = \
                            get_variables_coefficients_equations_for_submodel(specification_dict["_definition_"], "_definition_")
            definition["alias"]  = [VariableName(x).get_alias() for x in definition["variables"]]
            del specification_dict["_definition_"]
        for sub_model, submodel_spec in list(specification_dict.items()):
            variable, coefficient, equation, submodel, fixed_value, other_field = get_variables_coefficients_equations_for_submodel(
                                                                         submodel_spec, sub_model, definition)
            variables += variable
            coefficients += coefficient
            equations += equation
            submodels += submodel
            fixed_values += fixed_value
            for key, value in other_field.items():
                if key in other_fields:
                    other_fields[key] = concatenate((other_fields[key], value))
                else:
                    other_fields[key] = array(value)

    except Exception as e:
        logger.log_stack_trace()
        raise ValueError("Wrong specification format for model specification: %s" % e)

    if where(array(fixed_values) != 0)[0].size == 0: # no fixed values defined
        fixed_values = []
    return (array(variables), array(coefficients), array(equations, dtype="int16"), array(submodels, dtype="int16"), 
            array(fixed_values), other_fields)

def load_specification_from_dictionary(specification_dict):
    """See the doc string at get_specification_attributes_from_dictionary
    """
    variables, coefficients, equations, submodels, fixed_values, other_fields = get_specification_attributes_from_dictionary(specification_dict)
    return EquationSpecification(variables=variables, coefficients=coefficients, equations = equations, submodels = submodels, 
                                 fixed_values = fixed_values, other_fields=other_fields)

def get_variables_coefficients_equations_for_submodel(submodel_spec, sub_model, definition={}):
    variables = []
    coefficients = []
    fixed_values = []
    equations = []
    submodels = []
    other_fields = {}
    error = False
    if isinstance(submodel_spec, tuple) or isinstance(submodel_spec, list): # no equations or other fields given
        variables, coefficients, fixed_values, error = get_variables_coefficients_from_list(submodel_spec, definition)
    elif isinstance(submodel_spec, dict):
        name = submodel_spec.get('name', 'equation')
        if name.startswith('equation'): # by default the dictionary is on an equation level
            variables, coefficients, fixed_values, equations, error = get_variables_coefficients_equations_from_dict(submodel_spec, 
                                                                                                              definition)
        else:
            del submodel_spec['name']
            other_fields['dim_%s' % name] = []
            for other_field_value, spec in submodel_spec.items():
                variable, coefficient, equation, submodel, fixed_value, other_field = \
                            get_variables_coefficients_equations_for_submodel(spec, sub_model, definition)
                variables += variable
                coefficients += coefficient
                equations += equation
                submodels += submodel
                fixed_values += fixed_value
                other_fields['dim_%s' % name] += len(variable)*[other_field_value]
                for key, value in other_field.items():
                    if key in other_fields:
                        other_fields[key] = concatenate((other_fields[key], value))
                    else:
                        other_fields[key] = array(value)
    else:
        logger.log_error("Error in specification of submodel %s." % sub_model)
        return ([],[],[],[],[],{})
    if error:
        logger.log_error("Error in specification of submodel %s" % sub_model)
    submodels = len(variables)*[sub_model]
    return (variables, coefficients, equations, submodels, fixed_values, other_fields)

def get_full_variable_specification_for_var_coef(var_coef, definition):
    """get full variable name from definition diectionary by looking up the alias""" 
    if ("variables" in list(definition.keys())) and (var_coef in definition["alias"]):
        i = definition["alias"].index(var_coef)
        variable = definition["variables"][i]
    else:
        variable = var_coef
        i = None
    return variable, i

def get_variables_coefficients_equations_from_dict(dict_spec, definition={}):
    variables = []
    coefficients = []
    fixed_values = []
    equations = []
    error = False
    
    speckeys = list(dict_spec.keys())
    if sum([isinstance(x, int) for x in speckeys]) == len(speckeys): # keys are the equations
        for eq, spec in dict_spec.items():
            variable, coefficient, fixed_value, error = get_variables_coefficients_from_list(
                                                                     spec, definition)
            if error:
                logger.log_error("Error in specification of equation %s" % eq)
            variables += variable
            coefficients += coefficient
            fixed_values += fixed_value
            equations += len(variable)*[eq]
    else:
        if "equation_ids" in dict_spec:
            equation_ids = dict_spec["equation_ids"]
            del dict_spec["equation_ids"]
        else:
            equation_ids = None
        
        for var, coef in list(dict_spec.items()):
            if not equation_ids:
                var_name, var_index = get_full_variable_specification_for_var_coef(var, definition)
                variables.append(var_name)
                if var_index is not None:
                    coefficients.append(definition["coefficients"][var_index])
                    fixed_values.append(definition["fixed_values"][var_index])
                else:
                    coefficients.append(coef)
                    fixed_values.append(0)
            elif type(coef) is list or type(coef) is tuple:
                for i in range(len(coef)):
                    if coef[i] != 0:
                        var_name, var_index = get_full_variable_specification_for_var_coef(var, definition)
                        variables.append(var_name)
                        if var_index is not None:
                            fixed_values.append(definition["fixed_values"][var_index])
                        else:
                            fixed_values.append(0)
                        coefficients.append(coef[i])
                        equations.append(equation_ids[i])
            else:
                logger.log_error("Wrong specification format for variable %s; \nwith equation_ids provided, coefficients must be a list or tuple of the same length of equation_ids" % var)
                error = True
    return (variables, coefficients, fixed_values, equations, error)

def get_variables_coefficients_from_list(list_spec, definition={}):
    variables = []
    coefficients = []
    fixed_values = []
    error = False
    
    for var_coef in list_spec:
        if isinstance(var_coef, str):
            #var_coef is just variables long names or alias
            var_name, var_index = get_full_variable_specification_for_var_coef(var_coef, definition)
            variables.append(var_name)
            if var_index is not None:
                coefficients.append(definition["coefficients"][var_index])
                fixed_values.append(definition["fixed_values"][var_index])
            else:
                coefficients.append(VariableName(var_coef).get_alias())
                fixed_values.append(0)
        elif isinstance(var_coef, tuple) or isinstance(var_coef, list):
            var_name, var_index = get_full_variable_specification_for_var_coef(var_coef[0], definition)
            variables.append(var_name)
            if len(var_coef) == 1: # coefficient name is created from variable alias
                coefficients.append(VariableName(var_coef[0]).get_alias())
                fixed_values.append(0)
            elif len(var_coef) > 1: # coefficient names explicitly given
                coefficients.append(var_coef[1])
                if len(var_coef) > 2: # third item is the coefficient fixed value 
                    fixed_values.append(var_coef[2])
                else:
                    fixed_values.append(0)
            else:
                logger.log_error("Wrong specification format for variable %s" % var_coef)
                error = True
        elif isinstance(var_coef, dict):
            var_name, var_index = get_full_variable_specification_for_var_coef(list(var_coef.keys())[0], definition)
            variables.append(var_name)
            coefficients.append(list(var_coef.values())[0])
            fixed_values.append(0)
        else:
            logger.log_error("Wrong specification format for variable %s" % var_coef)
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
        self.assertTrue(result['variable_name'][0] == variables[0], 'Error in equation_specification')
        self.assertTrue(result['variable_name'][1] == variables[1], 'Error in equation_specification')

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
        self.assertTrue(alltrue(result['nest'] == spec_data["nest"]), 'Error in equation_specification')
        self.assertTrue(alltrue(result['fixed_value'] == spec_data["fixed_value"]), 'Error in equation_specification')
        self.assertTrue(alltrue(result['sub_model_id'] == array([-2, -2, -2], dtype="int32")),
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
        self.assertTrue(alltrue(result == array([variables[0], 'xxx.my_new_variable', 'y.replaces_y'])),
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
        self.assertTrue(alltrue(coefs == array(["BPOP", "BINC", "BART", "BHWY", "BAGE"])),
                     msg = "Error in test_load_specification (coefficients)")
        self.assertTrue(alltrue(vars ==
                                 array(["population", "average_income", "is_near_arterial", "is_near_highway", "lage"])),
                     msg = "Error in test_load_specification (variables)")
        self.assertTrue(ma.allequal(subm, array([1, 1, 2, 2, 3])),
                     msg = "Error in test_load_specification (submodels)")
        self.assertTrue(fixedval.size == 0, msg = "Error in test_load_specification (fixed_values should be empty)")
        
        # add a variable with a fixed value coefficient
        specification[3].append(("constant", "C", 1))
        result = load_specification_from_dictionary(specification)
        fixedval = result.get_fixed_values()
        self.assertTrue(ma.allequal(fixedval, array([0, 0, 0, 0, 0, 1])), 
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
        self.assertTrue(alltrue(coefs == array(["BPOP", "BINC", "BAGE", "BART", "C", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition (coefficients)")
        self.assertTrue(alltrue(vars ==
                                 array(["population", "average_income", "lage", "is_near_arterial", "constant", 
                                        "is_near_highway"])),
                     msg = "Error in test_load_specification_with_definition (variables)")
        self.assertTrue(ma.allequal(subm, array([1, 1, 1, 2, 2, 2])),
                     msg = "Error in test_load_specification_with_definition (submodels)")
        self.assertTrue(ma.allclose(fixedval, array([0, 0, 0, 0, 1.5, 0])), 
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
        self.assertTrue(alltrue(coefs == array(["population", "average_income", "lage", "is_near_arterial", "BHWY"])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (coefficients)")
        self.assertTrue(alltrue(vars ==
                                 array(["population", "average_income", "lage", "is_near_arterial", "is_near_highway"])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (variables)")
        self.assertTrue(ma.allequal(subm, array([1, 1, 1, 2, 2])),
                     msg = "Error in test_load_specification_with_definition_with_implicit_coefficients (submodels)")
        # test data type
        self.assertTrue(subm.dtype.name == "int16",
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
        self.assertTrue(alltrue(coefs == array(["asc", "bart", "bpop", "binc"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (coefficients)")
        self.assertTrue(alltrue(vars == array(["constant",  "art", "pop", "inc"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (variables)")
        self.assertTrue(ma.allequal(eqs, array([1,1,1,2])),
                     msg = "Error in test_load_specification_with_definition_with_equations (equations)")
        self.assertTrue(alltrue(lvars == array(["constant",  
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
        self.assertTrue(alltrue(coefs == array(["bpop", "inc", "constant", "art",])),
                     msg = "Error in test_load_specification_with_definition_with_equations_v2 (coefficients)")
        self.assertTrue(alltrue(vars == array(["pop", "inc", "constant",  "art"])),
                     msg = "Error in test_load_specification_with_definition_with_equations (variables)")
        self.assertTrue(ma.allequal(eqs, array([1,1,1,2])),
                     msg = "Error in test_load_specification_with_definition_with_equations (equations)")
        self.assertTrue(alltrue(lvars == array(["pop = urbansim.gridcell.population", 
                                             "inc = urbansim.gridcell.average_income",
                                             "constant",  
                                             "art = urbansim.gridcell.is_near_arterial", 
                                            ])),
                     msg = "Error in test_load_specification_with_definition_with_equations (long names of variables)")

    def test_load_specification_with_definition_nests(self):
        specification = {
             "_definition_": [
                 ("pop = urbansim.gridcell.population", "bpop"),
                 "inc = urbansim.gridcell.average_income",
                 "art = urbansim.gridcell.is_near_arterial",
                 ],
              -2: {
                   'name': 'nest_id',
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
        other = result.get_other_fields()
 
        self.assertTrue(alltrue(coefs == array(["bpop", "inc", "constant", "art",])),
                     msg = "Error in test_load_specification_with_definition_nests (coefficients)")
        self.assertTrue(alltrue(vars == array(["pop", "inc", "constant",  "art"])),
                     msg = "Error in test_load_specification_with_definition_nests (variables)")
        self.assertTrue(ma.allequal(other['dim_nest_id'], array([1,1,1,2])),
                     msg = "Error in test_load_specification_with_definition_nests (nests)")

    def test_load_specification_with_definition_nest_and_equations(self):
        specification = {
             "_definition_": [
                 ("pop = urbansim.gridcell.population", "bpop"),
                 "inc = urbansim.gridcell.average_income",
                 "art = urbansim.gridcell.is_near_arterial",
                 ],
              -2: {
                   'name': 'nest_id',
                   1: {1: [
                     "pop", 
                     "inc", 
                     "constant" ],
                      2: [ "art"]
                      },
                   2: {3:["pop", 
                          "inc"
                          ]}
                             }
              }
        result = load_specification_from_dictionary(specification)
        vars = result.get_variable_names()
        coefs = result.get_coefficient_names()
        eqs = result.get_equations()
        other = result.get_other_fields()
 
        self.assertTrue(alltrue(coefs == array(["bpop", "inc", "constant", "art", "bpop", "inc"])),
                     msg = "Error in test_load_specification_with_definition_nest_and_equations (coefficients)")
        self.assertTrue(alltrue(vars == array(["pop", "inc", "constant",  "art", "pop", "inc"])),
                     msg = "Error in test_load_specification_with_definition_nest_and_equations (variables)")
        self.assertTrue(ma.allequal(eqs, array([1,1,1,2,3,3])),
                     msg = "Error in test_load_specification_with_definition_nest_and_equations (equations)")
        self.assertTrue(ma.allequal(other['dim_nest_id'], array([1,1,1,1,2,2])),
                     msg = "Error in test_load_specification_with_definition_nest_and_equations (nests)")
if __name__=='__main__':
    opus_unittest.main()

