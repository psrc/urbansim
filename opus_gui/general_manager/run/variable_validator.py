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


from opus_core.variables.variable_name import VariableName
from opus_gui.results_manager.run.indicator_framework_interface import IndicatorFrameworkInterface
from opus_gui.results_manager.run.opus_result_generator import OpusResultGenerator

class VariableValidator(object):
    def __init__(self, toolboxBase):
        self.toolboxBase = toolboxBase
        # maximum number of lines in the error report (to prevent overlong dialogs)
        self.max_lines = 12
        
    def validate(self, variables, ok_msg):
        parsing_successful, parsing_errors = self.check_parse_errors(variables)
        
        if not parsing_successful:
            errorString = "Parse errors: <br><br>  " + "<br><br>".join(parsing_errors)
            return (False, errorString)
                    
        data_successful, data_errors = self.check_data_errors(variables)

        if data_successful:
            return (True, ok_msg)
        else:
            errorString = "Errors executing expression on baseyear data: <br><br>  " + "<br><br>".join(data_errors)
            return False, errorString
        
        
    def check_parse_errors(self, variables):
        # check the variables in the expression library as indexed by the list 'variables'.
        errors = []
        for (var_name, dataset_name, use, source, expr)  in variables:
            # special case -- the 'constant' expression always passes
            if expr.strip()=='constant' and var_name=='constant':
                continue
            try:
                n = VariableName(expr)
                # check that the expression is of the correct form given the source
                # TODO: what if it's a constant?
                if source=='primary attribute':
                    if n.get_autogen_class() is not None:
                        errors.append("Error - this is parsing as an expression rather than as a primary attribute: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif n.get_dataset_name() is None:
                        errors.append("Error in primary attribute - missing dataset name: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif dataset_name!=n.get_dataset_name():
                        errors.append("Error in primary attribute - dataset name mismatch: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif n.get_package_name() is not None:
                        errors.append("Error in primary attribute - shouldn't have package name: (%s, %s): %s" % (var_name, dataset_name, expr))
                elif source=='expression':
                    if n.get_autogen_class() is None:
                        errors.append("Error - this doesn't seem to be an expression.  Maybe it should be a Python class or primary attribute?: (%s, %s): %s" % (var_name, dataset_name, expr))
                elif source=='Python class':
                    if n.get_autogen_class() is not None:
                        errors.append("Error - this is parsing as an expression rather than as a Python class reference: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif n.get_package_name() is None:
                        errors.append("Error - missing package name in Python class reference: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif n.get_dataset_name() is None:
                        errors.append("Error - missing dataset name in Python class reference: (%s, %s): %s" % (var_name, dataset_name, expr))
                    elif dataset_name!=n.get_dataset_name():
                        errors.append("Error - dataset name  mismatch in Python class reference: (%s, %s): %s" % (var_name, dataset_name, expr))
                else:
                    errors.append("Unknown source type %s: (%s, %s): %s" % (source, var_name, dataset_name, expr))
            except (SyntaxError, ValueError), e:
                errors.append("Parsing error: (%s, %s): %s" % (var_name, dataset_name, str(e)))
            # check whether there are too many errors; if so stop to prevent the list from getting too long
            if self._too_many_errors(errors):
                errors.append("[*** rest of error report truncated ***]")
                return False, errors
        return len(errors) == 0, errors


    def check_data_errors(self, variables):
        errors = []
        for (var_name, dataset_name, use, source, expr) in variables:
            if var_name=='constant':
                continue
            successful, error = self._test_generate_results(indicator_name = var_name, dataset_name = dataset_name, expression = expr, source = source)
            if not successful:
                errors.append("Expression %s could not be run on <br>dataset %s on the baseyear data.<br>Details:<br>%s"%(
                                var_name, dataset_name, str(error) )) 
            if self._too_many_errors(errors):
                errors.append("[*** rest of error report truncated ***]")
                return False, errors
        return len(errors) == 0, errors
    
    def _too_many_errors(self, errors):
        # count how many lines there will be in the error report, and if over the max, return true
        lines = 0
        for e in errors:
            lines = lines + e.count('<br>') + 2
        return lines>self.max_lines
        
    def _test_generate_results(self, indicator_name, dataset_name, expression, source):
        
        interface = IndicatorFrameworkInterface(self.toolboxBase)
        node, vals = interface.xml_helper.get_element_attributes(node_name = 'base_year_data', 
                                                                 child_attributes = ['start_year'],
                                                                 node_type = 'source_data')
        years = [int(str(vals['start_year']))]

        result_generator = OpusResultGenerator(self.toolboxBase)
        result_generator.set_data(
               source_data_name = 'base_year_data',
               indicator_name = indicator_name,
               dataset_name = dataset_name,
               years = years,
               indicator_definition = (expression, source))
        
        try:
            result_generator.run(raise_exception = True)
            return True, None
        except Exception, e:
            return False, e
