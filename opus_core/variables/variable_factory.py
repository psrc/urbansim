# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable_family_name_translator import VariableFamilyNameTranslator
from opus_core.variables.variable_name import VariableName
from opus_core.misc import DebugPrinter
from opus_core.logger import logger
from opus_core.variables.lag_variable_parser import LagVariableParser

class VariableFactory(object):
    """Class for creating an instance of class Variable from a string that specifies the variable name.
    It should be used by calling the method 'get_variable'.  Each variable should be implemented as one of:
      - a class with a name of the variable, which should be placed in a module of the same name as the class
      - an expression
      - an alias that has a corresponding expression in the aliases.py file in the variables directory for that dataset
    Beware: the methods of this class are class methods, not object methods.
    """
    
    # Class dictionary holding the expression library.  The keys in the dictionary are pairs 
    # (dataset_name, variable_name) and the values are the corresponding expressions.
    # This starts out as an empty dictionary, and can be set using the set_expression_library method.
    _expression_library = {}
    def set_expression_library(self, lib):
        VariableFactory._expression_library = lib

    def get_variable(self, variable_name, dataset, quiet=False, debug=0, index_name=None):
        """Returns an instance of class Variable. 
        'variable_name' is an instance of class VariableName. 
        'dataset' is an object of class Dataset to which the variable belongs to. 
        In case of an error in either importing the module or evaluating its constructor, 
        the method returns None.
        If quiet is True no warnings are printed.
        index_name is used for lag variables only.
        """
        lag_attribute_name = None
        lag_offset = 0
            
        if not isinstance(debug, DebugPrinter):
            debug = DebugPrinter(debug)
            
        if variable_name.get_autogen_class() is not None:
            # variable_name has an autogenerated class -- just use that
            variable_subclass = variable_name.get_autogen_class()
            substrings = ()
        else:
            # either find the variable name in the expression library (if present), in an appropriate 'aliases' file, 
            # or load our variable class as 'variable_subclass' using an import statement
            short_name = variable_name.get_short_name()
            dataset_name = variable_name.get_dataset_name()
            package_name = variable_name.get_package_name()
            # if there isn't a package name, first look in the expression library (if there is a package name, look elsewhere)
            if package_name is None:
                e = VariableFactory._expression_library.get( (dataset_name,short_name), None)
                if e is not None:
                    v = VariableName(e)
                    return VariableFactory().get_variable(v, dataset, quiet=quiet, debug=debug)
            # not in the expression library - next look in the appropriate 'aliases' file, if one is present
            try:
                stmt = 'from %s.%s.aliases import aliases' % (package_name, dataset_name)
                exec(stmt)
            except ImportError:
                aliases = []
            for a in aliases:
                # for each definition, see if the alias is equal to the short_name.  If it is,
                # then use that definition for the variable
                v = VariableName(a)
                if v.get_alias() == short_name:
                    return VariableFactory().get_variable(v, dataset, quiet=quiet, debug=debug)

            lag_variable_parser = LagVariableParser()
            if lag_variable_parser.is_short_name_for_lag_variable(short_name):
                lag_attribute_name, lag_offset = lag_variable_parser.parse_lag_variable_short_name(short_name)
                true_short_name = "VVV_lagLLL"
                substrings = (package_name, lag_attribute_name, lag_offset, dataset_name, index_name)
                directory_path = 'opus_core.variables'
                
            else:             
                if package_name is None:
                    raise LookupError("Incomplete variable specification for '%s.%s' (missing package name)." 
                                      % (dataset_name, short_name))
                
                directory_path = '%s.%s' % (package_name,dataset_name)
                    
                true_short_name, substrings = VariableFamilyNameTranslator().\
                        get_translated_variable_name_and_substring_arguments(directory_path, short_name)
                
            module = '%s.%s' % (directory_path, true_short_name)
            try:
                ev = "from %s import %s as variable_subclass" % (module, true_short_name)
                debug.print_debug("Evaluating '" + ev + "'.",12)
                exec(ev)
                debug.print_debug("Successful.", 12)
            except ImportError:
                if not quiet:
                    from opus_core.simulation_state import SimulationState
                    time = SimulationState().get_current_time()
                    raise NameError("Opus variable '%s' does not exist for dataset '%s' in year %s" % 
                                    (true_short_name, directory_path, time))
                return None
        
        try:
            var_class = variable_subclass(*substrings)
        except:
            logger.log_error("Could not initialize class of variable %s." % variable_name.get_expression())
            logger.log_stack_trace()
            raise
        var_class.set_dataset(dataset)
        return var_class
    
    
from opus_core.tests import opus_unittest

### TODO: Write some tests!
class VariableFactoryTests(opus_unittest.OpusTestCase):
    def test(self):
        pass
        
if __name__ == '__main__': 
    opus_unittest.main() 
