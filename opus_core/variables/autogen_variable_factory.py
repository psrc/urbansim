# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# Note: even if PyDev complains that some of these imports are unused, generally they ARE
# in fact used when executing the generated code.
from sets import Set
import parser
from types import TupleType
from opus_core.variables.variable import Variable
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.variables.variable_name import VariableName, autogenvar_prefix
from opus_core.variables.dummy_name import DummyName
from opus_core.variables.dummy_dataset import DummyDataset, make_aggregation_call
from opus_core.variables.parsetree_functions import parsetree_to_string, parsetree_substitute
from opus_core.variables.parsetree_matcher import match
from opus_core.variables.parsetree_patterns import *

# import all of the functions that can be used in expression definitions
# (these are then also available in the autogenerated class)
from opus_core.variables.functions import *
# import numpy types (for use in astype() calls in expressions)
# these also need to be listed in the _named_constants class variable defined below
from numpy import bool8, int8, uint8, int16, uint16, int32, uint32, int64, uint64
from numpy import float32, float64, complex64, complex128, longlong
# allow the where function to be used directly (without qualifying it as numpy.where)
from numpy import where

class AutogenVariableFactory(object):
    """Class for generating the information held in a VariableName, in particular 
    the automatically defined class.
    """
    
    _named_constants = ["True", "False", "bool8", "int8", "uint8", "int16", "uint16", "int32", 
        "uint32", "int64", "uint64", "float32", "float64", "complex64", "complex128", "longlong"]
    
    # datasets whose name ends in _constant_suffix are treated as constant datasets
    _constant_suffix = '_constant'
    
    # counter for automatically-generated class names
    _autogen_counter = 0

    def __init__(self, expr):
        # expr is a string that is the expression being compiled into a variable
        self._expr = expr
        (tree, alias) = self._parse_expr()
        # expr_parsetree is a Python parse tree for self._expr
        self._expr_parsetree = tree
        # alias is either None, or a string that is the alias for the expression
        self._alias = alias
        # the remaining instance variables are set by generate_variable_name_tuple (if called)
        #
        # self._dataset_names is a tuple of datasets for which this expression is being evaluated.
        # Except for expressions for interaction sets, all of the qualified references at the
        # top level (not in aggregate or disaggregate calls) must be to the same dataset, and
        # after analyzing the expression self._dataset_names should be a tuple of length 1, which
        # will be the name of that dataset.  (An exception is if the expression just references
        # primary attributes, without a qualifying dataset.  Right now that's legal in expressions
        # but probably should be disallowed.)  
        # For interaction sets, from the expression we can determine the names of the component
        # datasets (n1 and n2).  The name of the interaction set will be either n1_x_n2 or n2_x_n1,
        # but we just determine the tuple (n1,n2) rather than trying to determine
        # that the dataset name is n1_x_n2 or n2_x_n1.  (Actually it's almost certainly n1_x_n2, if 
        # n1 is used first in the expression, but we don't try to guess.)
        self._dataset_names = ()
        # dependents is a set of dependents for expr.  Each element in 'dependents' 
        #     is a tuple (package,dataset,shortname).  For attributes named with just the
        #     un-qualified name, package and dataset will be None.  (This would be the case for
        #     primary attributes, and also other already-existing attributes in the dataset.)
        #     For dataset_qualified attributes, package will be None.  For example, for
        #     attributes of one of the component datasets of an interaction set, package will
        #     be None, and dataset will be the name of either the first or second component dataset.
        #     The other case of dataset_qualified attributes is for a variable to be aggregated.
        self._dependents = Set()
        # literals is a set of strings that should be compiled as literals, so that the expression
        # will evaluate correctly.  
        self._literals = Set()
        self._uses_number_of_agents  = False
        self._number_of_agents_receivers = Set()
        # aggregation_calls is a set of calls to aggregation/disaggregation methods.
        #     Each element of aggregation_calls is a tuple 
        #     (receiver, method, package, dataset_to_aggregate, variable_to_aggregate, [intermediate_datasets], operation)
        #     For example the call 'faz.aggregate(urbansim.gridcell.population, intermediates=[zone], function=sum' would result in the tuple
        #     ('faz', 'aggregate', 'urbansim', 'gridcell', 'population', ['zone'], 'sum')
        #     If the package is omitted this value is None.
        #     If the list of intermediate datasets or operation are omitted these values are None.
        # For aggregate_all intermediate_datasets is always [].
        # Disaggregation is the same, except that operation is always None.
        self._aggregation_calls = Set()
        # parsetree_replacements is a dictionary mapping parse tree fragments in the original
        # parsetree for self._expr to other tree fragments with which they should be replaced
        self._parsetree_replacements = {}

    def generate_variable_name_tuple(self):
        """return a tuple (package_name, dataset_names, short_name, alias, autogen_class)
        corresponding to my expression."""
        # Hack: always generate a new variable class if there is an alias, unless the expression is just a
        # reference to a variable and the alias is equal to its shortname  (See note below.)  In theory we 
        # shouldn't need a new class if we are just providing an alias for fully-qualified variable, 
        # dataset-qualified variable, or an attribute; but fixing this would require that datasets
        # keep a dictionary of additional aliases, since the alias is used as the name of the attribute.
        # This change should be made sometime when there is a rewrite of Dataset.)
        #
        # Note regarding an expression that is just a reference to a variable and the alias is equal to its shortname:
        # this handles cases like 
        #       population = urbansim.gridcell.population
        # in which the alias is the same as the shortname.  In this case we just drop the alias.
        #
        # first check if expr is a fully-qualified variable, dataset-qualified variable, or an attribute
        same, vars = match(EXPRESSION_IS_FULLY_QUALIFIED_VARIABLE, self._expr_parsetree)
        if same and (self._alias is None or vars['shortname']==self._alias):
            return (vars['package'], (vars['dataset'],), vars['shortname'], None, None)
        same, vars = match(EXPRESSION_IS_DATASET_QUALIFIED_VARIABLE, self._expr_parsetree)
        if same and (self._alias is None or vars['shortname']==self._alias):
            return (None, (vars['dataset'],), vars['shortname'], None, None)
        same, vars = match(EXPRESSION_IS_ATTRIBUTE, self._expr_parsetree)
        if same and (self._alias is None or vars['shortname']==self._alias):
            return (None, (), vars['shortname'], None, None)
        # it's a more complex expression -- need to generate a new variable class
        (short_name, autogen_class) = self._generate_new_variable()
        return (None, self._dataset_names, short_name, self._alias, autogen_class)
    
    def get_parsetree(self):
        return self._expr_parsetree

    def _parse_expr(self):
        # Parse self._expr and return the parsetree and alias.
        # If self._expr is just an expression, then alias will be None.
        # If self._expr is an assignment v=ex then alias will be v, and
        # expr_parsetree will be the parsetree for expr.
        # If the parse raises a syntax error, just let that be handled
        # by the regular error handler.
        # Raise an exception if the expression doesn't match either an expression
        # or a statement (this would happen if the expression consists of multiple
        # statements, which parses correctly).
        # First try parsing self._expr as a single expression (no assignment).
        # If self._expr is an assignment, this will raise an exception.
        full_tree = parser.ast2tuple(parser.suite(self._expr))
        same, vars = match(FULL_TREE_EXPRESSION, full_tree)
        if same:
            return (vars['expr'], None)
        same, vars = match(FULL_TREE_ASSIGNMENT, full_tree)
        if same:
            return (vars['expr'], vars['alias'])
        raise ValueError, "invalid expression (perhaps multiple statements?): " + self._expr
    
    # loooong comment regarding the _generate_variable method that follows:
    # generate a new class for a variable to compute the value of self._expr 
    # (for use when expr is a compound expression).  First consider the case
    # where there isn't an alias for self._expr.  As an example, suppose
    # that expr is ln_bounded(urbansim.gridcell.population)
    # Then the generated class is
    #
    #    class autogenvar034(Variable):
    #        def dependencies(self):
    #            return ['urbansim.gridcell.population']
    #        def name(self):
    #            return 'ln_bounded(urbansim.gridcell.population)'
    #        def compute(self, dataset_pool):
    #            urbansim = DummyName()
    #            urbansim.gridcell = DummyDataset(self, 'gridcell', dataset_pool)
    #            urbansim.gridcell.population = self.get_dataset().get_attribute('population')
    #            return ln_bounded(urbansim.gridcell.population)
    #
    # If the expression includes an alias, for example pop = ln_bounded(urbansim.gridcell.population),
    # then the code is all the same as above, except that the final return statement is replaced with
    #
    #            pop = ln_bounded(urbansim.gridcell.population)
    #            return pop
    #
    # The name of the class is generated (there is a class variable autogen_number that starts at 0
    # and gets incremented each time it's used in a new name).  
    #
    # The dependencies method is constructed by parsing the expression and finding all of the 
    # other variables that it references, and putting those into the returned list.
    #
    # The compute method ends with a return statement that just returns expr.  To make this work,
    # we need to provide local bindings for e.g. urbansim.gridcell.population.  We bind a
    # local variable (named urbansim in the example) to an instance of DummyName, whose sole 
    # purpose in life is to have an attribute gridcell (and maybe other attributes if there are
    # multiple dependencies).  We then add a population attribute to urbansim.gridcell, which
    # is bound to the value of the appropriate dataset attribute.  For the get_attribute call to
    # get the value of the population attribute, we use the short version of the name -- its value
    # should already have been computed.
    #
    # There are some subtleties regarding environments.  The new class is defined in the module
    # in which this class (AutogenVariableFactory) is defined, and the new name will be bound in
    # locals.  The compute() method has access to the globals in this environment (i.e. the 
    # environment of AutogenVariableFactory), and so the imports at the front of this class definition
    # make Variable and all of the functions in opus_core.variables.functions available in
    # the new class.  In particular writers of expressions have access to the functions in opus_core.variables.functions
    def _generate_new_variable(self):
        self._analyze_tree(self._expr_parsetree)
        self._analyze_dataset_names()
        classname = autogenvar_prefix + str(self._autogen_counter)
        AutogenVariableFactory._autogen_counter = self._autogen_counter+1
        # now build up a string 'classexpr' that will be used to define the new class
        classexpr = 'class %s (Variable): \n%s%s%s' % \
            (classname, self._generate_dependencies_method(), self._generate_name_method(), self._generate_compute_method())
        # Now create the new class by executing the string we've built up.
        # This class will be defined in the current environment (might want to change that later).
        exec(classexpr)
        # Return a tuple consisting of the name of the new class and the new class
        return (classname, locals()[classname])
    
    def _analyze_tree(self, tree):
        # add the dependents of parse tree 'tree' to 'dependents', and any variables that are to
        # be bound to a string of the same name to 'literals'. 
        # if tree isn't a tuple, we're at a leaf -- no dependents in that case
        if type(tree) is not TupleType:
            return
        # if tree matches the fully qualified variable subpattern, then add that variable as the dependent
        same, vars = match(SUBPATTERN_FULLY_QUALIFIED_VARIABLE, tree)
        if same:
            # it's a fully-qualified variable (maybe raised to a power)
            self._dependents.add( (vars['package'], vars['dataset'], vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_FULLY_QUALIFIED_VARIABLE_WITH_CAST, tree)
        if same:
            # it's a fully-qualified variable with a cast (maybe raised to a power)
            self._dependents.add( (vars['package'], vars['dataset'], vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_DATASET_QUALIFIED_ATTRIBUTE, tree)
        if same:
            self._dependents.add( (None, vars['dataset'], vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_DATASET_QUALIFIED_ATTRIBUTE_WITH_CAST, tree)
        if same:
            self._dependents.add( (None, vars['dataset'], vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_ATTRIBUTE, tree)
        if same:
            if vars['shortname'] not in self._named_constants:
                # it's an attribute (maybe raised to a power)
                self._dependents.add( (None, None, vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_ATTRIBUTE_WITH_CAST, tree)
        if same:
            self._dependents.add( (None, None, vars['shortname']) )
            return
        same, vars = match(SUBPATTERN_METHOD_CALL_WITH_ARGS, tree)
        if same:
            self._analyze_method_call(vars['receiver'], vars['method'], vars['args'])
            return
        same, vars = match(SUBPATTERN_METHOD_CALL_WITH_ARGS_WITH_CAST, tree)
        if same:
            self._analyze_method_call(vars['receiver'], vars['method'], vars['args'])
            return
        # Check for arguments to a method or function.  Since there may be a variable number
        # of arguments, just check whether the first thing in the tree is the symbol for an
        # argument list.  If so the rest of the tuple is the arguments.
        same, vars = match(SUBPATTERN_ARGLIST, tree[0])
        if same:
            # this is a list of arguments for a method or function
            self._analyze_arguments(tree[1:])
            return
        # otherwise recursively descend through the tuple (ignoring the first element, which is
        # an integer identifying the production in the grammar)
        for sub in tree[1:]:
            self._analyze_tree(sub)

    def _analyze_method_call(self, receiver, method, args):
        if method=='number_of_agents':
            self._analyze_number_of_agents_method_call(receiver, method, args)
        elif method in ['aggregate', 'disaggregate', 'aggregate_all']: 
            self._analyze_aggregation_method_call(receiver, method, args)
        else:
            # it's some other kind of method call - just analyze the args (omit the initial symbol.arglist token)
            self._analyze_arguments(args[1:])

    def _analyze_number_of_agents_method_call(self, receiver, method, args):
        same, vars = match(SUBPATTERN_NUMBER_OF_AGENTS, args)
        if not same:
            raise ValueError, "syntax error for number_of_agents function call"
        self._uses_number_of_agents  = True
        self._number_of_agents_receivers.add(receiver)
        self._literals.add(vars['agent'])

    def _analyze_aggregation_method_call(self, receiver, method, args):
        same, vars = match(SUBPATTERN_AGGREGATION, args)
        if not same:
            raise ValueError, "syntax error for aggregation method call"
        arg_dict = self._get_arguments( ('arg1', 'arg2','arg3'), ('aggr_var', 'intermediates','function'), vars )
        if 'aggr_var' not in arg_dict:
            raise ValueError, "syntax error for aggregation method call (problem with argument for variable being aggregated)"
        same1, vars1 = match(SUBPATTERN_FULLY_QUALIFIED_VARIABLE_ARG, arg_dict['aggr_var'])
        if same1:
            # the aggregated variable is a fully-qualified name
            pkg = vars1['package']
            dataset = vars1['dataset']
            attr = vars1['shortname']
        else:
            same2, vars2 = match(SUBPATTERN_DATASET_QUALIFIED_VARIABLE_ARG, arg_dict['aggr_var'])
            if same2:
                # the aggregated variable is a dataset-qualified name
                pkg = None
                dataset = vars2['dataset']
                attr = vars2['shortname']
            else:
                # The thing being aggregated is an expression.  Generate a new autogen variable for that expression,
                # and use the autogen variable in the aggregation call.
                subexpr = arg_dict['aggr_var']
                newvar = VariableName(parsetree_to_string(subexpr))
                pkg = None
                dataset = newvar.get_dataset_name()
                if dataset is None:
                    raise ValueError, "syntax error for aggregation method call - could not determine dataset for variable being aggregated"
                attr = newvar.get_short_name()
                replacements = {'dataset': dataset, 'attribute': attr}
                newvar_tree = parsetree_substitute(DATASET_QUALIFIED_VARIABLE_TEMPLATE, replacements)
                self._parsetree_replacements[subexpr] = newvar_tree
        if 'intermediates' in arg_dict:
            # make sure that it really is a list
            s, v = match(SUBPATTERN_LIST_ARG, arg_dict['intermediates'])
            if not s:
                raise ValueError, "syntax error for aggregation method call (list of intermediate datasets not a list?)"
            intermediates = self._extract_names(arg_dict['intermediates'])
            self._literals.update(intermediates)
        else:
            intermediates = ()
        if 'function' in arg_dict:
            s,v = match(SUBPATTERN_NAME_ARG, arg_dict['function'])
            if not s:
                raise ValueError, "syntax error for aggregation method call (problem with the function argument in the call)"
            op = v['name']
            self._literals.add(op)
        else:
            op = None
        self._aggregation_calls.add( (receiver, method, pkg, dataset, attr, intermediates, op) )

    # extract all the names from tree and return them in a tuple
    def _extract_names(self, tree):
        same, vars = match(SUBPATTERN_NAME, tree)
        if same:
            return (vars['name'],)
        else:
            ans = ()
            for sub in tree[1:]:
                ans = ans + self._extract_names(sub)
            return ans

    # Extract arguments from parse tree pieces.
    # arg_pattern_names is a list of names of the arguments that
    # were extracted by the 'match' function.  These names index
    # into arg_dict, which is the dictionary of values returned by 'match'.
    # formals is a list (or tuple) of formal argument names (strings).
    # return a dictionary with keys = names of arguments, values = values of those arguments
    def _get_arguments(self, arg_pattern_names, formals, arg_dict):
        formals_list = list(formals)  # make a copy, since we'll alter this
        # keyword_mode becomes true once we start seeing keywords on the arguments
        keyword_mode = False
        result = {}
        for a in arg_pattern_names:
            if a not in arg_dict:
                # we've gone through all of the actual arguments that were supplied
                return result
            same, vars = match(SUBPATTERN_ARGUMENT, arg_dict[a])
            if not same:
                raise ValueError, 'parse error for arguments'
            if 'part2' in vars:
                # change to keyword mode if necessary (if we're already there, that's ok)
                keyword_mode = True
            elif keyword_mode:
                # we're in keyword mode, but no keyword on this arg
                raise ValueError, 'non-keyword argument found after keyword argument'
            if keyword_mode:
                # get the actual keyword out of part1, and the value out of part2
                kwd_same, kwd_vars = match(SUBPATTERN_NAME_ARG, vars['part1'])
                if not kwd_same:
                    raise ValueError, 'parse error for arguments'
                kwd = kwd_vars['name']
                val = vars['part2']
                if kwd not in formals_list:
                    raise ValueError, 'unknown keyword %s' % kwd
                formals_list.remove(kwd)
                result[kwd] = val
            else:
                kwd = formals_list[0]
                formals_list = formals_list[1:]
                val = vars['part1']
                result[kwd] = val         
        return result
    
    # Analyze the dataset names to try and determine the principal dataset name.  If this expression
    # uses more than one dataset it must be for an interaction set.
    def _analyze_dataset_names(self):
        for pkg, ds, short in self._dependents:
            if ds is not None:
                self._analyze_one_dataset_name(ds)
        for receiver, method, pkg, aggregated_dataset, aggregated_attr, intermediates, op in self._aggregation_calls:
            self._analyze_one_dataset_name(receiver)
        for receiver in self._number_of_agents_receivers:
            self._analyze_one_dataset_name(receiver)

    def _analyze_one_dataset_name(self, name):
        # if 'name' ends in self._constant_suffix ignore it as far as determining the expression's dataset name
        if name is None or name.endswith(self._constant_suffix):
            pass
        elif name not in self._dataset_names:
            self._dataset_names = self._dataset_names + (name,)

    # Analyze the arguments for a function or method call.  This is a separate method from _analyze_tree
    # because we need to treat the keywords in keyword arguments properly and not think they are variable names.
    # Precondition: there is at least one arg in the tuple
    def _analyze_arguments(self, args):
        same, vars = match(SUBPATTERN_ARGUMENT, args[0])
        if same:
            # if part2 exists then part1 is the corresponding keyword - just discard part1
            # otherwise part1 is the argument itself
            if 'part2' in vars:
                self._analyze_tree(vars['part2'])
            else:
                self._analyze_tree(vars['part1'])
        else:
            raise StandardError, 'internal error - problem analyzing arguments in expression'
        if len(args)>1:
            # skip the comma (which is args[1]) and analyze the remaining arguments
            # (since this passed the Python parser we know that the tree is syntactically correct - no 
            # need to check that the comma is there)
            self._analyze_arguments(args[2:])

    def _generate_dependencies_method(self):
        # m is the dependencies method being built up
        dm = 4*' ' + 'def dependencies(self): \n' + 8*' ' + 'return ['
        need_comma = False
        for pkg, ds, short in self._dependents:
            # if the dataset name ends in self._constant_suffix don't add it to the dependencies
            if ds is None or not ds.endswith(self._constant_suffix):
                if need_comma:
                  dm = dm + ', '
                else:
                    need_comma = True  # put in a comma the next time around the loop
                if ds is None:
                    dm = dm + 'self.get_dataset().get_dataset_name()+".%s"' % short
                elif pkg is None:
                    dm = dm + '"%s.%s"' % (ds, short)
                else:
                    dm = dm + '"%s.%s.%s"' % (pkg, ds, short)
        # add dependency info for aggregation variables, if any
        for receiver, method, pkg, aggregated_dataset, aggregated_attr, intermediates, op in self._aggregation_calls:
            if need_comma:
                dm = dm + ', '
            else:
                need_comma = True
            dm = dm + '"%s"' % make_aggregation_call(method, pkg, aggregated_dataset, aggregated_attr, op, intermediates)
        dm = dm + ']' + '\n'
        return dm
    
    def _generate_name_method(self):
        # generate a method to return the name of this variable (which will be its defining expression)
        return 4*' ' + 'def name(self): \n' + 8*' ' + 'return "%s" \n' %self._expr
    
    def _generate_compute_method(self):
        compute_method = 4*' ' + 'def compute(self, dataset_pool): \n'
        # Generate local bindings for variables.  We need to avoid overwriting an existing binding,
        # so keep track of which have already been generated.  For example, when we first encounter
        # urbansim.gridcell.population, we need to generate all of the bindings (as described in the
        # long comment before this method).  After that, if we encounter urbansim.household.has_children
        # we need to add a household attribute to urbansim -- but not reinitialize the variable
        # urbansim itself.  Then if we find urbansim.gridcell.population_density we should just add
        # the population_density attribute to urbansim.gridcell (and not reinitialize either urbansim
        # or urbansim.gridcell).
        already_generated = Set()
        for pkg, ds, short in self._dependents:
            # if the dataset name ends in self._constant_suffix, get the dataset out of the dataset pool; otherwise it is self.get_dataset()
            if ds is not None and ds.endswith(self._constant_suffix):
                getter = 'dataset_pool.get_dataset("%s").get_attribute("%s")' % (ds,short)
            else:
                getter = 'self.get_dataset().get_attribute("%s")' % short
            if ds is None:
                # the dependent is an unqualified attribute name
                compute_method = compute_method + 8*' ' + '%s = %s \n' % (short, getter)
            elif pkg is None:
                if (None,ds) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s = DummyDataset(self, "%s", dataset_pool) \n' % (ds, ds)
                    already_generated.add( (None,ds) )
                compute_method = compute_method + 8*' ' + '%s.%s = %s \n' % (ds, short, getter)
            else:
                if pkg not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s = DummyName() \n' % pkg
                    already_generated.add(pkg)
                if (pkg,ds) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s.%s = DummyDataset(self, "%s", dataset_pool) \n' % (pkg, ds, ds)
                    already_generated.add( (pkg,ds) )
                compute_method = compute_method + 8*' ' + '%s.%s.%s = %s \n' % (pkg, ds, short, getter)
        # generate bindings for aggregation variables
        for receiver, method, pkg, aggregated_dataset, aggregated_attr, intermediates, op in self._aggregation_calls:
            if (None,receiver) not in already_generated:
                compute_method = compute_method + 8*' ' + '%s = DummyDataset(self, "%s", dataset_pool) \n' % (receiver, receiver)
                already_generated.add( (None,receiver) )
            if pkg is None:
                if (None,aggregated_dataset) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s = DummyDataset(self, "%s", dataset_pool) \n' % (aggregated_dataset, aggregated_dataset)
                    already_generated.add( (None,aggregated_dataset) )
                if (aggregated_dataset,aggregated_attr) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s.%s = DummyName() \n' % (aggregated_dataset, aggregated_attr)
                    already_generated.add( (aggregated_dataset,aggregated_attr) )
                compute_method = compute_method + 8*' ' + '%s.%s.name = ("%s", "%s") \n' % \
                    (aggregated_dataset, aggregated_attr, aggregated_dataset, aggregated_attr)
            else:
                if pkg not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s = DummyName \n' % pkg
                    already_generated.add(pkg)
                if (pkg,aggregated_dataset) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s.%s = DummyDataset(self, "%s", dataset_pool) \n' % (pkg, aggregated_dataset, aggregated_dataset)
                    already_generated.add( (pkg,aggregated_dataset) )
                if (pkg,aggregated_dataset,aggregated_attr) not in already_generated:
                    compute_method = compute_method + 8*' ' + '%s.%s.%s = DummyName() \n' % (pkg, aggregated_dataset, aggregated_attr)
                    already_generated.add( (pkg,aggregated_dataset,aggregated_attr) )
                compute_method = compute_method + 8*' ' + '%s.%s.%s.name = ("%s", "%s", "%s") \n' % \
                        (pkg, aggregated_dataset, aggregated_attr, pkg, aggregated_dataset, aggregated_attr)
        for receiver in self._number_of_agents_receivers:
            if (None,receiver) not in already_generated:
                compute_method = compute_method + 8*' ' + '%s = DummyDataset(self, "%s", dataset_pool) \n' % (receiver, receiver)
                already_generated.add( (None,receiver) )
        # generate bindings for literals if needed
        for lit in self._literals:
            if (None,lit) not in already_generated:
                compute_method = compute_method + 8*' ' + lit + ' = DummyName() \n'
                # don't really need this, but it will make the method more robust if we add some other code late that uses already_generated
                already_generated.add( (None,lit) )
            compute_method = compute_method + 8*' ' + '%s.name = "%s" \n' % (lit, lit)
        # If we need to replace parts of the parse tree, do the replacements, and turn the parse tree
        # back into a string to generate the method.  Otherwise just use the original expression.
        # (We could always turn the tree back into a string I guess ...)
        if len(self._parsetree_replacements)==0:
            newexpr = self._expr
        else:
            newtree = parsetree_substitute(self._expr_parsetree, self._parsetree_replacements)
            newexpr = parsetree_to_string(newtree)
            # the parse tree doesn't include the assignment statement that sets up the alias
            if self._alias is not None:
                newexpr = self._alias + ' = ' + newexpr
        # If alias is None, we can just return the expression.  If alias is not none, then expr will bind 
        # the alias to the desired value, so execute expr, and return the value in the alias.
        if self._alias is None:
            compute_method = compute_method + 8*' ' + 'return ' + newexpr + '\n'
        else:
            compute_method = compute_method + 8*' ' + newexpr + '\n'
            compute_method = compute_method + 8*' ' + 'return ' + self._alias + '\n'
        return compute_method
