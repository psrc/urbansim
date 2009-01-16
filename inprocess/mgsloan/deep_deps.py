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

factory = VariableFactory()
config = XMLConfiguration("/home/mgsloan/opus/project_configs/eugene_gridcell_default.xml")

lib = config.get_expression_library()
factory.set_expression_library(lib)

#TODO: there seems to be an issue with the (xml)dictionary approach -there can be
# multiple, indexed, submodels. This only seems to handle the first

#this collects all the variables models depend on
var_list = []
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
                    var_list.append(lib[k])
        var_tree.append((x, l))

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
        return None

#get a dependency tree for a variable given its name
def get_named_deps(name):
    varclass = get_var(name)
    if(varclass == None): return (name, [])
    return get_deps(varclass)

def get_deps(inp):
    result_others = []
    dependencies_list = inp.get_current_dependencies()
    for i in range(len(dependencies_list)):
        dep_item = dependencies_list[i][0]
        if isinstance(dep_item, str):
            result_others.append(get_named_deps(dep_item))
        else:
            print "Attribute!"
    return (inp.name(), result_others)

def remove_leaves(inp):
    ret = []
    for x in inp:
        if len(x[1]) > 0:
            ret.append((x[0], remove_leaves(x[1])))
    return ret

def elim_dups(xs):
    ret = []
    for x in xs:
        if x in ret: continue
        ret.append(x)
    return ret;

def deps_graph(trees):
    ret = []
    def write_edges(tree):
        #print tree[0]
        #ret.append("    \"" + tree[0] + "\" ]")
        for x in tree[1]:
            ret.append("    \"" + tree[0] + "\" -> \"" + x[0] + "\"")
            write_edges(x)
    map(write_edges, trees)
    ret = elim_dups(ret)
    ret.insert(0, "digraph G {")
    ret.append("rankdir=LR\n")
    return ret

temp = remove_leaves(map(get_named_deps, var_list)) + var_tree
#print temp
ret3 = deps_graph(temp)
for x in var_tree:
    ret3.append(x[0] + "[ shape=box ]")
ret3.append("}")
print '\n'.join(ret3)

#print deps_graph([get_deps(Dummy())])

#print deps_graph([("Hello", [("how", [("are", [("you?",[])])])]), ("What's up,", [("how", [("are", [("you?",[])])])])])
