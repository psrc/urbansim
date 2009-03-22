# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_box import AttributeBox
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable import Variable
from opus_core.variables.variable_name import VariableName
from opus_core.variables.variable_factory import VariableFactory
from opus_core.variables.autogen_variable_factory import AutogenVariableFactory
from numpy import where, array
from opus_core.configurations.xml_configuration import XMLConfiguration

import os, sys
from optparse import OptionParser

from opus_core.third_party.pydot import Dot, Edge, Node

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
        #TODO: if we update to ElementTree 1.3, use
        # model_manager/model_system//specification/[@type='submodel']/variables
        for x in config._find_node('model_manager/model_system//specification'):
            l = []
            for y in x:
                if y.get('type') == 'submodel':
                    t = y.find('variables')
                    if len(t) > 0:
                        for z in config._convert_variable_list_to_data(t[0]):
                            for k in lib.keys():
                                if k[1] == z:
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
    
    # returns a list of VariableNames a model depends on
    def get_model_var_list(self, name):
        ret = []
        def rec(xs):
            for x in xs:
                ret.append(VariableName(x[0]))
                rec(x[1])
        rec(map(self.get_dep_tree_from_name, extract_leaves(self.get_model_vars(name)[1])))
        return elim_dups(ret)
    
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

        ret = elim_dups(ret)
        ret.insert(0, "digraph G {")
        ret.append("    " + ("rankdir=LR\n" if lr else "") + "dpi=%d" % dpi)
        return ret
    
    #generates an image file (using pydot) from a tree
    def graph_tree(self, fi, trees, lr, dpi):
        dot = Dot(rankdir=("LR" if lr else "TB"), dpi=str(dpi))
        def write_edges(tree):
            for x in tree[1]:
                dot.add_edge(Edge(tree[0], x[0]))
                write_edges(x)
            if len(tree) > 2:
                dot.add_node(Node(tree[0], shape = {"primary":"diamond", "model":"box"}[tree[2]]))
        map(write_edges, trees)
        dot.write_png(fi + ".png")
    
    #return latex-formatted table of a model's depndencies
    def model_table(self, model):
        vs = groupBy(self.query.get_model_var_list(model), lambda x: x.get_dataset_name())
        ret = []
        for k in vs:
            if k == None: continue
            ret += [k,"\\begin{tabular}{|l|l|l|}","\\hline", \
             "\\textbf{Column Name} & \\textbf{Data Type} & \\textbf{Description} \\"]
            for x in vs[k]:
                ret.append("\\hline")
                ret.append("%s & integer & \\" % x.get_short_name())
            ret.append("\\hline")
            ret.append("\\end{tabular}")
            ret.append("")
        return '\n'.join(ret)

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
#if given a function uses that to generate the identifier for each item
def elim_dups(xs, f=None):
    ret = []
    if f == None:
        for x in xs:
            if x in ret: continue
            ret.append(x)
    else:
        test_list = []
        for x in xs:
            v = f(x)
            if v in test_list: continue
            ret.append(x)
            test_list.append(v)
    return ret

def groupBy(xs, f):
    ret = {}
    for x in xs:
        v = f(x)
        if(v in ret):
            ret[v].append(x)
        else:
            ret[v] = [x]
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
#python dependency_query.py -xeugene/configs/eugene_gridcell.xml
#This outputs each model in seperate gv files, and processes them with dot
#
#python dependency_query.py -xeugene/configs/eugene_gridcell.xml -oout
#This outputs all of the models and their dependencies into out.gv/.png
#
#python dependency_query.py -xeugene/configs/eugene_gridcell.xml -oout -vurbansim.gridcell.total_improvement_value
#This outputs out.gv, and runs dot to yield out.png, with the dependencies of urbansim.gridcell.total_improvement_value charted.
#
#python dependency_query.py -xeugene/configs/eugene_gridcell.xml -oout -mland_price_model
#This outputs out.gv, and runs dot to yield out.png, with the dependencies of land_price_model charted.
#
#python dependency_query.py -xeugene/configs/eugene_gridcell.xml -ltable.tex -mland_price_model
#This outputs a table.tex file which is a template for a table of the land_price_model dependencies.
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
    parser.add_option("-l", "--latex", dest="latex", default=None,
                      help="latex output file")

    (options, args) = parser.parse_args()
    
    if options.xml_configuration == None:
        raise "Requires an xml configuration argument."

    chart = DependencyChart(XMLConfiguration(options.xml_configuration))
    #print chart.model_table(options.model)
    #temp = chart.query.vars_tree(chart.query.var_list)
    #print pretty_tree(chart.query.all_models_tree())
    
    auto = AutogenVariableFactory("(urbansim_parcel.parcel.building_sqft/(parcel.parcel_sqft).astype(float32)).astype(float32)")
    auto._analyze_tree(auto._expr_parsetree)
    auto._analyze_dataset_names()
    print(auto._generate_compute_method())
    
    if options.latex != None:
        if options.model == None: raise "latex output requires specification of model"
        write_file(options.latex, chart.model_table(options.model))
    elif options.variable != None:
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
