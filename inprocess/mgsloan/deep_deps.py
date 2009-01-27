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

# This isn't intentionally overengineered into many functions, that's just the influence of haskell ;)

# Here, trees are represented as tuples, where the first element is the label, and the second is a list of more tuples

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_box import AttributeBox
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.variables.variable_factory import VariableFactory
from numpy import where, array
from opus_core.configurations.xml_configuration import XMLConfiguration
from optparse import OptionParser
import os
import sys

factory = VariableFactory()

#loads an xml configuration file, and returns a list of models paired with a list of vars they depend upon
#also sets the nasty evil factory global's expression library
def get_config_dep_tree(fi):

    config = XMLConfiguration(fi)

    lib = config.get_expression_library()
    factory.set_expression_library(lib)

    #TODO: there seems to be an issue with the (xml)dictionary approach -there can be
    # multiple, indexed, submodels. This only seems to retrieve the first

    #this collects all the variables models depend on
    var_tree = []
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
            var_tree.append((x, l))
    return var_tree

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

#given a name, return an instance of Variable
def get_var(name):
    var = VariableName(name)
    dataset = var.get_dataset_name()
    try:
        return factory.get_variable(var, create_fake_dataset(dataset), quiet=True)
    except LookupError:
#        print "LOOKUP ERROR: " + name
        return None

#get a dependency tree for a variable given its name
def get_dep_tree_from_name(name):
    varclass = get_var(name)
    if(varclass == None): return (name, [], "shape = diamond")
    return get_dep_tree(varclass)

#returns a dependency tree given a particular variable
def get_dep_tree(inp):
    result_others = []
    dependencies_list = inp.get_current_dependencies()
    for x in dependencies_list:
        dep_item = x[0]
        if isinstance(dep_item, str):
            result_others.append(get_dep_tree_from_name(dep_item))
        else:
            print "Attribute!"
    return (inp.name(), elim_dups(result_others))

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
                    map(process, x[1])
    process(inp)
    return ret

#eliminates duplicates in a list.  
def elim_dups(xs):
    ret = []
    for x in xs:
        if x in ret: continue
        ret.append(x)
    return ret;

#processes a tree into a list of lines, in dot format
#final } is left off, so that more attributes may be added.
def tree_to_dot(trees):
    ret = []
    def write_edges(tree):
        for x in tree[1]:
            ret.append("    \"" + tree[0] + "\" -> \"" + x[0] + "\"")
            write_edges(x)
        if len(tree) > 2:
            ret.append("    \"" + tree[0] + "\"[ " + tree[2] + " ]")
    map(write_edges, trees)
    ret = elim_dups(ret)
    ret.insert(0, "digraph G {")
    ret.append("    rankdir=LR\ndpi=60")
    return ret

def all_models_tree(var_tree):
    return map(get_dep_tree_from_name, extract_leaves(var_tree)) \
         + map(lambda x: (x[0],x[1],"shape=box"), var_tree)

def find(f, seq):
  for item in seq:
    if f(item): 
      return item

def lookup_model(var_tree, name):
    model = find(lambda x: x[0] == name, var_tree)
    if model == None:
        raise "Model " + name + " not found."
    else:
        return model

def model_tree(model):
    return map(get_dep_tree_from_name, extract_leaves(model[1])) \
            + [(model[0], model[1],"shape=box")]

def vars_tree(var_list):
    return map(get_dep_tree_from_name, extract_leaves(var_list))

def write_file(fi, txt):
    f = open(fi, 'w')
    f.write(txt)
    f.close()

def graph_tree(fi, tree):
    out = tree_to_dot(tree)
    out.append("}")
    write_file(fi + ".gv", '\n'.join(out))
    os.system("dot -Tpng -o" + fi + ".png " + fi + ".gv")

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
    (options, args) = parser.parse_args()
    
    if options.xml_configuration == None:
        raise "Requires an xml configuration argument."

    var_tree = get_config_dep_tree(options.xml_configuration)
    
    tree = []
    out_file = options.output
    if options.variable != None:
        graph_tree(options.variable if options.output == None else options.output,
                   vars_tree([options.variable]))
    elif options.model != None:
        graph_tree(options.model if options.output == None else options.output,
                   model_tree(lookup_model(var_tree, options.model)))
    else:
        if options.output == None:
            for x in var_tree:
                print "Processing " + x[0] + "..."
                graph_tree(x[0], model_tree(x))
        else:
            graph_tree(options.output, all_models_tree(var_tree))
