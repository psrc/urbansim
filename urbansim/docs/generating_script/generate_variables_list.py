# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import sys

import inspect

from pydoc import ModuleScanner 
from opus_core.logger import logger

class GenerateVariableInformationHTML(object):
    
    header = \
"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>

<head>
<meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
<link href="book.css" rel="stylesheet" type="text/css">
<title>Model Variables\</title>
</head>

<body>
<!-- HEAD BANNER BEGINS HERE :: to be placed immediately below body tag -->

<table border="0" cellspacing="0" width="100%">
<tbody>
  <tr>

    <td><a href="http://www.urbansim.org/"><img src="../../opus_core/docs/images/new-logo-medium.gif" border="0"
    height="45" width="105"></a></td>
    <td align="right" valign="bottom"><!--#include virtual="/docs/searchbar.html" --> <br>
    </td>
  </tr>
  <tr>
    <td colspan="2" class="breadcrumbbox" bgcolor="#eeeeee" width="100%"><a href="index.html">UrbanSimPython
    module</a> &gt; Model Variables</td>

  </tr>
</tbody>
</table>
<!-- HEAD BANNER ENDS HERE -->

<h2><font color="#FF0000">Introduction needs to be updated</font></h2>

<h1>Model Variables</h1>
<p>Many of the UrbanSim models use functions over
sets of variables to make decisions (for example, UrbanSim uses logit models
with utility functions, and hedonic regressions). 
Starting with UrbanSim 2.1, the set of
variables used in each model is configurable via the model
configuration database tables. Each variable is defined by an object
extending the Variable class.</p>
<blockquote><i>A note on nomenclature</i>: the objects are called &quot;terms&quot;
because they consist of a &quot;variable&quot; and a &quot;coefficient&quot;

together. The class defines only the &quot;variable&quot; portion; the
&quot;coefficient&quot; is specified in the model
configuration database tables. This documentation loosely interchanges
&quot;variable&quot; and &quot;term&quot;.</blockquote>
<p>UrbanSim includes a predefined set of variable classes. Users may use these
classes, define their own classes, or both. 

<p> The remainder of this page is a
list of the predefined variables. The Java class corresponding to each model
variable is &quot;org.urbansim.models.variables.TERM_xxx&quot; where xxx is the
variable name, e.g., &quot;org.urbanim.models.variables.TERM_building_age&quot;
for the building_age variable.</p>

<p>Each variable computes its value from an agent, a choice, and/or some
neighborhood of grid cells. The specific type of agents and choices, differ for
each model. For example, the Household Location Choice's agent is a <i>household</i>
and choice is a <i>grid cell</i>, so the Household Location Choice model can use
any variable whose agent is listed in the table either as empty (don't care) or
specifically as &quot;household&quot;, and whose choice is listed in the table
either as empty (don't care) or specifically as &quot;grid cell&quot;. The same
Household Location Choice model cannot use the <code>
same_sector_employment_within_walking_distance</code> variable, because its agent is a
&quot;job&quot; rather than a &quot;household&quot;.</p>
"""

    footer = """ \
    </body>
</html>"""
    
    def generate_variables_table(self, root_module="urbansim", output_path=""):
        """ Generate a list of all variables into HTML table format"""  
        module_list = self.variable_modules_sorted(root_module)
        f = open(output_path+"variable_table.html", 'w')
        f.write(self.__class__.header)
        f.write('<table border="1">\n')
        f.write('<tr>\n\t<th>Variable Name</th>\n\t<th>Module</th>\n\t<th>Notes</th>\n</tr>\n')
        for name in module_list:
            (doc_string, cls_name) = self.get_doc_string('.'.join(name))
            if doc_string == None: doc_string = ''
            f.write('<tr>\n\t<td>'+cls_name+ 
                    '</td>\n\t<td>'+name[-2]+
                    '</td>\n\t<td>'+doc_string +'</td>\n</tr>\n')
        f.write('</table>\n')
        f.write(self.__class__.footer)
        f.close()
        logger.log_status('html file output completed')
        
    def generate_variables_table_sorted_by_module(self, root_module="urbansim", output_path=""):
        variable_list = self.variable_modules_sorted(root_module)
        
        module_list = []
        while variable_list != []:
            module_to_get = variable_list[0][-2]
            module_list.append(self.filter_and_remove(lambda x: x[-2] == module_to_get, variable_list))
            
        module_list.sort(lambda x, y: (int)(x[0][-2] > y[0][-2]) - (int)(x[0][-2] < y[0][-2]))
            
        f = open(output_path+"variable_module_tables.html", 'w') 
        f.write(self.__class__.header)
        for module in module_list:
            f.write('<h3>'+ module[0][-2] +'</h3>\n')
            f.write('<table border="1">\n')
            f.write('<tr>\n\t<th>Variable Name</th>\n\t<th>Notes</th>\n</tr>\n')           
            for name in module:
                (doc_string, cls_name) = self.get_doc_string('.'.join(name))
                if doc_string == None: doc_string = ''
                f.write('<tr>\n\t<td>'+cls_name+ 
                        '</td>\n\t<td>'+doc_string +'</td>\n</tr>\n')
            f.write('</table>\n<br>\n')
        f.write(self.__class__.footer)
        f.close()
        logger.log_status('html file output completed')
        
    def get_doc_string(self, module_name):
        """ Assume there are no more than one classes in module that extend Variable."""
        module = eval(module_name)
        (cls_name, cls) = filter(lambda (cls_name, cls): issubclass(cls, opus_core.variables.variable.Variable) and cls.__module__ == module_name, 
                                   inspect.getmembers(module, inspect.isclass))[0]
        return (cls.__doc__ or  ' ', cls_name)

    def filter_and_remove(self, a_function, a_list):
        filtered_list = filter(a_function, a_list)
        [a_list.remove(x) for x in filtered_list]
        return filtered_list
    
    def select_distinct_module_types(self, module_list):
        modules = []
        for m in module_list:
            if not m[-2] in modules:
                modules.append(m[-2])
        return modules

    def variable_modules_sorted(self, opus_directory_name):
        """ return a list {(file_path, module_name)} of classes that extend variable.
        module_name is the name of the Opus module, e.g. 'urbansim' .""" 
        def callback_to_record_if_subclass_of_Variable(path, module_name, description):
            try:
                if module_name.endswith('__init__'): 
                    return
                __import__(module_name)
                the_module = eval(module_name)           # TODO: Is this a security hole?
                for a_class in inspect.getmembers(the_module, inspect.isclass):
                    if a_class[1] != opus_core.variables.variable.Variable and \
                        issubclass(a_class[1], opus_core.variables.variable.Variable):
                        module_list.append(module_name)
                        return
            except:
                logger.log_status("Problem loading module " + module_name)
        
        module_list=[]
        ModuleScanner().run(callback_to_record_if_subclass_of_Variable, opus_directory_name + ".")
    
        module_list = map(lambda t: t.split('.'), module_list)
        module_list.sort(lambda x, y: (int)(x[-1] > y[-1]) - (int)(x[-1] < y[-1]))
        return module_list

if __name__ == '__main__':
    GenerateVariableInformationHTML().generate_variables_table(output_path="../")
    GenerateVariableInformationHTML().generate_variables_table_sorted_by_module(output_path="../")