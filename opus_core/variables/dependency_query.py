#
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

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_box import AttributeBox
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.variables.variable_factory import VariableFactory
from numpy import where, array
from opus_core.configurations.xml_configuration import XMLConfiguration

import os, sys
from optparse import OptionParser

class DependencyQuery:
    def __init__(self, config):
        self.factory = VariableFactory()

        lib = config.get_expression_library()
        self.factory.set_expression_library(lib)

        #TODO: there seems to be an issue with the (xml)dictionary approach -there can be
        # multiple, indexed, submodels. This only seems to retrieve the first

        #this collects all the variables models depend on
        self.var_tree = []
        self.var_list = []
        for x in config.get_section('model_manager/model_system'):
            spec = config.get_section('model_manager/model_system/' + x + '/specification')
            if spec != None:
                fst = spec.keys()[0]
                if fst != 'submodel': spec = spec[fst]
                l = []
                for y in spec['submodel']['variables']:
                    for k in lib.keys():
                        if k[1] == y:
                            l.append((lib[k], []))
                            self.var_list.append(lib[k])
                self.var_tree.append((x, l))

    #given a name, return an instance of Variable
    def get_var(self, name):
        #creates a fake dataset, required for variable resolution
        def create_fake_dataset(dataset_name):
            storage = StorageFactory().get_storage('dict_storage')
            
            storage.write_table(
                table_name='fake_dataset',
                table_data={
                    'id':array([], dtype='int32')
                    }
                )

            dataset = Dataset(in_storage=storage, in_table_name='fake_dataset', dataset_name=dataset_name, id_name="id")
            return dataset
        var = VariableName(name)
        dataset = var.get_dataset_name()
        try:
            return self.factory.get_variable(var, create_fake_dataset(dataset), quiet=True)
        except LookupError:
            print "LOOKUP ERROR: " + name
            return None
    
    #given a name, returns the tree with the model at the root, and the vars it depends on as leaves
    def get_model_vars(self, name):
        def find(f, seq):
            for item in seq:
                if f(item): 
                    return item
        model = find(lambda x: x[0] == name, self.var_tree)
        if model == None:
            raise "Model " + name + " not found."
        else:
            return model

    #get a dependency tree for a variable given its name
    def get_dep_tree_from_name(self, name):
        varclass = self.get_var(name)
        if(varclass == None): return (name, [], "primary")
        return self.get_dep_tree(varclass)

    #returns a dependency tree given a particular variable
    def get_dep_tree(self, inp):
        result_others = []
        dependencies_list = inp.get_current_dependencies()
        for x in dependencies_list:
            dep_item = x[0]
            if isinstance(dep_item, str):
                result_others.append(self.get_dep_tree_from_name(dep_item))
            else:
                print "Attribute!"
        return (inp.name(), elim_dups(result_others))

    def all_models_tree(self):
        return map(self.get_dep_tree_from_name, extract_leaves(self.var_tree)) \
             + map(lambda x: (x[0],x[1],"model"), self.var_tree)

    def model_tree(self, name):
        model = self.get_model_vars(name)
        return map(self.get_dep_tree_from_name, extract_leaves(model[1])) \
                + [(model[0], model[1],"model")]

    def vars_tree(self, vl):
        return map(self.get_dep_tree_from_name, extract_leaves(vl))

class DependencyChart:
    def __init__(self, config):
        self.query = DependencyQuery(config)
    
    def graph_variable(self, out, var, lr=True, dpi=60):
        self.graph_tree(var if out == None else out, self.query.vars_tree([var]), lr, dpi)
    def graph_model(self, out, model, lr=True, dpi=60):
        self.graph_tree(model if out == None else out, self.query.model_tree(model), lr, dpi)
    def graph_all(self, out, lr=True, dpi=60):
        self.graph_tree(out, self.query.all_models_tree(), lr, dpi)
    
    #processes a tree into a list of lines, in dot format
    #final } is left off, so that more attributes may be added.
    def tree_to_dot(self, trees, lr=True, dpi=60):
        ret = []
        trans = {"primary":"[ shape=diamond ]", "model":"[ shape=box ]"}
        def write_edges(tree):
            for x in tree[1]:
                ret.append("    \"" + tree[0] + "\" -> \"" + x[0] + "\"")
                write_edges(x)
            if len(tree) > 2:
                ret.append("    \"" + tree[0] + "\"" + trans[tree[2]])
        map(write_edges, trees)
        ret = elim_dups(ret)
        ret.insert(0, "digraph G {")
        ret.append("    " + ("rankdir=LR\n" if lr else "") + "dpi=%d" % dpi)
        return ret

    def graph_tree(self, fi, tree, lr, dpi):
        out = self.tree_to_dot(tree, lr, dpi)
        out.append("}")
        write_file(fi + ".gv", '\n'.join(out))
        os.system("dot -Tpng -o" + fi + ".png " + fi + ".gv")

#Utility Funcs

#removes the leaves of a tree constructed of tuples and lists.
#assumes the input is a list, and that the 2nd part of the tuple is the nested content.
def remove_leaves(inp):
    ret = []
    for x in inp:
        if isinstance(x, tuple) and len(x[1]) > 0:
            lst = list(x)
            lst[1] = remove_leaves(lst[1])
            ret.append(tuple(lst))
    return ret

#returns a list of all the leaves of an input tree
def extract_leaves(inp):
    ret = []
    def process(xs):
        for x in xs:
            if (not isinstance(x, tuple)) and (not isinstance(x, list)):
                ret.append(x)
            elif isinstance(x, tuple):
                if len(x[1]) == 0:
                    ret.append(x[0])
                else:
                    process(x[1])
    process(inp)
    return ret

#eliminates duplicates in a list.  
def elim_dups(xs):
    ret = []
    for x in xs:
        if x in ret: continue
        ret.append(x)
    return ret

# writes a text file
def write_file(fi, txt):
    f = open(fi, 'w')
    f.write(txt)
    f.close()

def pretty_tree(tree):
    ret = []
    def helper(ix, xs):
        ret.append("  " * ix + xs[0])
        for x in xs[1]:
            helper(ix + 1, x)
    for x in tree:
        helper(0, x)
    return '\n'.join(ret)

#To use:
#
#python deep_deps.py -xeugene/configs/eugene_gridcell.xml
#This outputs each model in seperate gv files, and processes them with dot
#
#python deep_deps.py -xeugene/configs/eugene_gridcell.xml -oout
#This outputs all of the models and their dependencies into out.gv/.png
#
#python deep_deps.py -xeugene/configs/eugene_gridcell.xml -oout -vurbansim.gridcell.total_improvement_value
#This outputs out.gv, and runs dot to yield out.png, with the dependencies of urbansim.gridcell.total_improvement_value charted.
#
#python deep_deps.py -xeugene/configs/eugene_gridcell.xml -oout -mland_price_model
#This outputs out.gv, and runs dot to yield out.png, with the dependencies of land_price_model charted.
#
#if -o is not given and -v or -m are, the variable or model name are used for the .gv/.png

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                      help="file name of xml configuration")
    parser.add_option("-v", "--variable", dest="variable", default=None,
                      help="variable for which you want to chart dependencies")
    parser.add_option("-m", "--model", dest="model", default=None,
                      help="model for which you want to chart dependencies")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="output image")
# TODO
#    parser.add_option("-b", "--nobase", dest="nobase", default=None,
#                      help="indicates to strip out base variables")

    (options, args) = parser.parse_args()
    
    if options.xml_configuration == None:
        raise "Requires an xml configuration argument."

    chart = DependencyChart(XMLConfiguration(options.xml_configuration))

    temp = chart.query.vars_tree(chart.query.var_list)
    print pretty_tree(temp)
    
    if options.variable != None:
        chart.graph_variable(options.output, options.variable)
    elif options.model != None:
        chart.graph_model(options.output, options.model)
    else:
        if options.output == None:
            for x in chart.query.var_tree:
                print "Processing " + x[0] + "..."
                chart.graph_model(None, x[0])
        else:
            chart.graph_all(options.output)
