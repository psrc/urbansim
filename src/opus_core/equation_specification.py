#
# Opus software. Copyright (C) 1998-2007 University of Washington
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
                 fixed_values=None, other_fields=None, in_storage=None, out_storage=None):
        """  variables - array of names of variables that are to be connected to coefficients.
            coefficients (coef. names), equations and submodels are arrays of the same length as variables or empty arrays.
            variables[i] is  meant to belong to coefficient[i], equations[i], submodels[i].
            fixed_values is an array with coeffcient values that should stay constant in the estimation. 
            other_fields should be a dictionary holding other columns of the specification table.
            The actual connection is done by SpecifiedCoefficients.

        """
        
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
        
        self.out_storage.write_dataset(local_resources)
#        self.out_storage.write_table(table_name=local_resources["out_table_name"],
#            table_data=values,
#            )

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
            return self.get_equations().max()
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
                variables[i] = VariableName(new_expr)
        self.variables = tuple(variables)
        
#Functions
class SpecLengthException(Exception):
    def __init__(self, name):
        self.args = "Something is wrong with the size of the specification object " + name + "!"

from numpy import alltrue, ma
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    def test_write_method_for_expressions(self):

        variables = ("x = y.disaggregate(mydataset.my_variable, intermediates=[myfaz])",
                     "z = y.disaggregate(mydataset.my_variable, intermediates=[myfaz, myzone])")
        coefficients = ('c1', 'c2')
        #db_host_name='localhost'
        #db_user_name=os.environ['MYSQLUSERNAME']
        #db_password =os.environ['MYSQLPASSWORD']
        #database = "test_database"
        #con = OpusDatabase(hostname=db_host_name, username=db_user_name,
        #               password=db_password, database_name=database)
        #storage = StorageFactory().get_storage('mysql_storage', storage_location=con)
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
        self.assert_(ma.allequal(result, array([variables[0], 'xxx.my_new_variable', 'y.replaces_y'])),
                     "Error in replace_varibles")

if __name__=='__main__':
    opus_unittest.main()

