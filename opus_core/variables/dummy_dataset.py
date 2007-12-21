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

from numpy import array
from opus_core.variables.variable_name import VariableName

class DummyDataset(object):
    """Instances of DummyDataset are used to construct local environments for evaluating the expression
    in autogenerated variable classes.  They are used for the dataset part of a fully-qualified or
    dataset-qualified name.  They also implement the aggregation and disaggregation methods used in
    the expression language."""
    
    def __init__(self, var, name, dataset_pool):
        self._var = var
        self._name = name
        self._dataset_pool = dataset_pool

    def aggregate(self, aggr_var, intermediates=[], function=None):
        dataset = self._get_dataset()
        if len(aggr_var.name)==2:
            (base_dataset, base_attribute) = aggr_var.name
            base_pkg = None
        else:
            (base_pkg, base_dataset, base_attribute) = aggr_var.name
        if function is None:
            function_name = None
        else:
            function_name = function.name
        if intermediates==[]:
            aggregated_dataset = base_dataset
            dependent_attribute = base_attribute
        else:
            intermediate_names = map(lambda n: n.name, intermediates)
            expr = make_aggregation_call('aggregate', base_pkg, base_dataset, base_attribute, function_name, intermediate_names)
            aggregated_dataset = intermediates[-1].name
            dependent_attribute = VariableName(expr).get_alias()
        ds = self._dataset_pool.get_dataset(aggregated_dataset)
        ds.compute_one_variable_with_unknown_package(dataset.get_id_name()[0], dataset_pool=self._dataset_pool)
        if function is None:
            result = dataset.aggregate_dataset_over_ids(ds, attribute_name=dependent_attribute)
        else:
            result = dataset.aggregate_dataset_over_ids(ds, function=function_name, attribute_name=dependent_attribute)
        self._var.add_and_solve_dependencies([ds._get_attribute_box(dataset.get_id_name()[0])], dataset_pool=self._dataset_pool)
        return self._coerce_result(result, dataset)

    def aggregate_all(self, aggr_var, function=None):
        dataset = self._var.get_dataset()
        # unlike the other aggregation/disaggregation functions, aggregate_all can't be used on the
        # component of an interaction set (the modelers said this doesn't make sense)
        if dataset.get_dataset_name()!=self._name:
            raise ValueError, 'mismatched dataset names for aggregate_all (perhaps trying to use aggregate_all on the component of an interaction set?)'
        if len(aggr_var.name)==2:
            (aggregated_dataset, dependent_attribute) = aggr_var.name
        else:
            (pkg, aggregated_dataset, dependent_attribute) = aggr_var.name
            # note that pkg is ignored
        ds = self._dataset_pool.get_dataset(aggregated_dataset)
        if function is None:
            return array(ds.aggregate_all(attribute_name=dependent_attribute))
        else:
            return array(ds.aggregate_all(function=function.name, attribute_name=dependent_attribute))

    def disaggregate(self, aggr_var, intermediates=[]):
        dataset = self._get_dataset()
        if len(aggr_var.name)==2:
            (base_dataset, base_attribute) = aggr_var.name
            base_pkg = None
        else:
            (base_pkg, base_dataset, base_attribute) = aggr_var.name
        if intermediates==[]:
            disaggregated_dataset = base_dataset
            dependent_attribute = base_attribute
        else:
            intermediate_names = map(lambda n: n.name, intermediates)
            expr = make_aggregation_call('disaggregate', base_pkg, base_dataset, base_attribute, None, intermediate_names)
            disaggregated_dataset = intermediates[-1].name
            dependent_attribute = VariableName(expr).get_alias()
        ds = self._dataset_pool.get_dataset(disaggregated_dataset)
        result = dataset.get_join_data(ds, dependent_attribute)
        self._var.add_and_solve_dependencies([dataset._get_attribute_box(ds.get_id_name()[0])], dataset_pool=self._dataset_pool)
        return self._coerce_result(result, dataset)
    
    def number_of_agents(self, agent_name):
        dataset = self._get_dataset()
        agents = self._dataset_pool.get_dataset(agent_name.name)
        id_name = dataset.get_id_name()[0]
        if id_name not in agents.get_attribute_names(): # attribute not loaded yet
            agents.get_attribute(id_name)
        self._var.add_and_solve_dependencies([agents._get_attribute_box(id_name)], dataset_pool=self._dataset_pool)
        result = dataset.sum_dataset_over_ids(agents, constant=1)
        return self._coerce_result(result, dataset)
    
    def _get_dataset(self):
        # get the actual dataset associated with this dummy dataset.  For ordinary datasets, this will be the same as
        # the dataset for self._var; but for interaction sets, it might be one of the components
        d = self._var.get_dataset()
        if d.get_dataset_name()==self._name:
            return d
        else:
            return d.get_dataset_named(self._name)
        
    def _coerce_result(self, result, dataset):
        # result is the 1-d array that is the result of an aggregation or disaggregation operation.
        # If this is a dummy dataset for an ordinary dataset, just return it.  However, if this
        # is a dummy dataset for a component of an interaction set, turn it into the correct 2-d array.
        d = self._var.get_dataset()
        if dataset.get_dataset_name()==d.get_dataset_name():
            return result
        else:
            owner_dataset, index = d.get_owner_dataset_and_index(dataset.get_dataset_name())
            return result[index]
        

# helper function for aggregate/disaggregate
def make_aggregation_call(method, pkg, dataset, shortname, op, intermediates):
    """generate a string that represents a call to an aggregate/disaggregate method.
    method is the name of the operation (aggregate, aggregate_all, disaggregate)
    pkg is the package for the variable being aggregated or None
    dataset and shortname are the dataset and name for the variable being aggregated
    op is the function used for the aggregation (e.g. sum), or None.
    intermediates is a list of intermediate datasets.
    """
    if pkg is None:
        aggregated = '%s.%s' % (dataset, shortname)
    else:
        aggregated = '%s.%s.%s' % (pkg, dataset, shortname)
    if not intermediates:
        return aggregated
    elif len(intermediates)==1:
        new_intermediates = ''
    else:
        new_intermediates = ',intermediates=[%s' % intermediates[0]
        for n in intermediates[1:-1]:
            new_intermediates = new_intermediates + ',' + n
        new_intermediates = new_intermediates + ']'
    if op is None:
        op_part = ''
    else:
        op_part = ',function=%s' % op
    receiver = intermediates[-1]
    return '%s.%s(%s%s%s)' % (receiver, method, aggregated, new_intermediates, op_part)
