# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import copy, os, pprint
from numpy import array
from lxml.etree import ElementTree, tostring, fromstring, Element, _Comment
from opus_core.configuration import Configuration
from opus_core.configurations.xml_version import XMLVersion
from opus_core.version_numbers import minimum_xml_version, maximum_xml_version
from opus_core.opus_exceptions.xml_version_exception import XMLVersionException
from opus_core.variables.variable_name import VariableName
from opus_core.misc import directory_path_from_opus_path
from opus_core.logger import logger
import re

def is_comment(node):
    return isinstance(node, _Comment)

def is_no_comment(node):
    return not is_comment(node)

def only_no_comment(nodes):
    for node in nodes:
        if is_no_comment(node):
            yield node

def element_id(node):
    '''
    Get an id string for a given element
    @param node (Element) element to get id string for
    @return the id string for the given element (str)
    '''
    if node is None:
        return ''
    return '/%s:%s' % (node.tag if is_no_comment(node) else hash(node),
                       node.get('name') or '')

def node_identity_string(node):
    '''
    Get a string that is unique for this node. This string is assembled by taking the
    tag and the 'name' attribute (separated by a colon) for each node in the nodes path except the root.

    For example, the following XML structure will return the string '/parent:i am a parent/node:child'
        <root>
         <parent name="i am a parent">
          <node name="child" />
         </parent>
        </root>

    @param node (Element) the node to get id string for
    @return the id string (str)
    '''
    # Skip the XML root node (will be the same for all nodes in a project so it's redundant)
    if node.getparent() is None:
        return ''
    return node_identity_string(node.getparent()) + element_id(node)

def load_xml_file(filename):
    if not os.path.exists(filename):
        raise IOError("File %s does not exist" % filename)
    tree = ElementTree(file=filename)
    # don't strip comments anymore
    return tree

def get_variable_parts(variable_node):
    '''
    Return a tuple of (dataset, name, terse_name)
    '''
    terse_name = variable_node.get('terse_name')

    # this is to maintain support for variables specified in pre-2.0 XML
    name = variable_node.get('name')
    if variable_node.get('dataset') is not None:
        return (variable_node.get('dataset'), name, terse_name)
    # TODO not sure on how to deal with constants -- any suggestions?
    if name == 'constant':
        return (None, name, terse_name)
    if name.startswith('__'):
        return (None, name, terse_name)
    splitted_name = name.split('.')
    if len(splitted_name) < 2:
        raise SyntaxError('Variable does not have dataset attribute nor give the dataset in the '
                          'name attribute "%s"' % name)
    dataset, name = splitted_name[0], ''.join(splitted_name[1:])
    return (dataset.strip(), name.strip(), terse_name)

def get_variable_dataset_and_name(variable_node):
    ''' extract the dataset and the variable name from a node.
    if the node has an attribute 'dataset', the dataset is taken from there ande the whole name
    attribute is used for the name. Otherwise the word before the first period in the name attribute
    is assumed the be the dataset '''
    dataset, name, terse_name = get_variable_parts(variable_node)
    return (dataset, name)

def get_variable_name(variable_node):
    ''' short convenience method for getting just the variable name '''
    return get_variable_dataset_and_name(variable_node)[1]

def get_variable_dataset(variable_node):
    ''' short convenience method for getting just the variable dataset '''
    return get_variable_dataset_and_name(variable_node)[0]

class XMLConfiguration(object):
    """
    An XMLConfiguration is a kind of configuration that represents a project
    and that can be stored or loaded from an XML file.
    """

    def __init__(self, filename = None, default_directory=None, is_parent=False):
        """Initialize this configuration from the contents of the xml file named by 'filename'.
        Look first in the default directory if present; otherwise in the directory in which
        the Opus code is stored.  If is_parent is true, mark all of the nodes as inherited
        (either from this configuration or a grandparent).
        If filename is not given, the configuration is initalized to an empty tree."""
        self.full_filename = self._find_parent_file(filename, default_directory)
        # if self.full_filename doesn't exist, ElementTree will raise an IOError
        # self.tree is the xml tree (without any inherited nodes);
        # self.full_tree is the xml tree with all the inherited nodes as well
        # parent_map is a dictionary that can be used to work back up the XML tree
        # these are all set by the _initialize method
        self.tree = None
        self.full_tree = None
        self.inherited_tree = None
        self.parent_map = None
        self.first_writable_parent_file = None
        self.name = os.path.basename(self.full_filename).split('.')[0]
        self.pp = pprint.PrettyPrinter(indent=4)
        self.xml_version = XMLVersion()
        self.version_warning_message = '' # Accumulated version warning message from loading parents
        # If a filename was given; initialize from that file, otherwise create an empty conf
        if filename is not None and self.full_filename is not None:
            self.initialize_from_xml_file(is_parent)
        else:
            minimum_tree = ElementTree(Element('opus_project'))
            self._initialize(minimum_tree, is_parent)

    def _find_parent_file(self, filename, default_directory):
        full_filename = None
        if filename is not None:
            if default_directory is not None:
                f = os.path.join(default_directory, filename)
                if os.path.exists(f):
                    full_filename = f
            if full_filename is None:
                opus_core_dir = __import__('opus_core').__path__[0]
                workspace_dir = os.path.split(opus_core_dir)[0]
                full_filename = os.path.join(workspace_dir, filename)
        else:
            full_filename = ''
        return full_filename

    def initialize_from_xml_file(self, is_parent=False):
        """initialize (or re-initialize) the contents of this configuration from the xml file.
        If is_parent is true, mark all of the nodes as inherited
        (either from this configuration or a grandparent)."""
        # try to load the element tree
        logger.log_status("Loading XML configuration: %s" % self.full_filename)
        tree = load_xml_file(self.full_filename)
        self._initialize(tree, is_parent)

    def update(self, newconfig_str):
        """Update the contents of this configuration from the string newconfig_str
        (a string representing an xml configuration).  Ignore any temporary or
        inherited nodes in newconfig_str (this gets freshly initialized)."""
        # Note that this doesn't change the name of this configuration, or the full_filename
        str_io = StringIO.StringIO(newconfig_str)
        etree = ElementTree(file=str_io)
        # don't strip comments anymore
        # remove any old followers nodes
        for n in self.full_tree.getiterator():
            if n.get('followers') is not None:
                # unfortunately it doesn't look like ElementTree has a method for removing an attribute ....
                del n.attrib['followers']
        self._set_followers(etree.getroot(), self._get_parent_trees(), '')
        self._clean_tree(etree.getroot())
        self._initialize(etree, False)

    def get_section(self, path, name = None):
        """
        Extract a section from this xml configuration (via path) and convert it to a dictionary.
        If only the path is given, the node is selected by the tag with given path. If the name
        is also provided, the tag with given path and matching attribute: "name" is selected.

        @return the resulting dictionary or None if there is no such section.
        """
        return self.section_from_node(self._find_node(path, name))

    def section_from_node(self, node):
        """ Convert a node into dictionary format and return it. """
        if node is None:
            return None
        else:
            return Configuration(self._node_to_config(node))

    def get_expression_library(self):
        """Return a dictionary of variables defined in the expression library for this configuration.  The keys in the
        dictionary are pairs (dataset_name, variable_name) and the values are the corresponding expressions."""
        result = {}

        for var_node in self._find_node('general/expression_library/variable', get_all=True):
            # Add the variable to the dictionary, indexed by the pair (dataset,name)
            dataset, name = get_variable_dataset_and_name(var_node)
            result[(dataset,name)] = var_node.text.strip()
        return result

    def get_run_configuration(self, name, merge_controllers=True):
        """Extract the run configuration named 'name' from this xml project and return it.
        Note that one run configuration can inherit from another (in addition to the usual
        project-wide inheritance).  If merge_controllers is True, merge in the controller
        section into the run configuration.  If the configuration has a travel model configuration,
        insert that under 'travel_model_configuration'.  The travel model configuration is formed
        by merging the information from the travel model configuration sections in the model_manager
        and in the scenario.  If the configuration has an expression library, add that to the
        configuration under the key 'expression_library' """
        general_section = self.get_section('general')
        project_name = general_section['project_name']
        config = self.get_section('scenario_manager/scenario', name)
        if config is None:
            raise ValueError, "didn't find scenario named %s; " % name + \
                  "If you're restarting a run make sure there is a scenario_name column in " + \
                  "run_activity table of your services database."
        self._insert_expression_library(config)
        # Merge the information from the travel model configuration sections in the model_manager
        model_manager_tm_config = self.get_section('model_manager/travel_model_configuration')
        if model_manager_tm_config is not None:
            s = config.get('travel_model_configuration', None)
            model_manager_tm_config.merge(s)
            config['travel_model_configuration'] = model_manager_tm_config
        if merge_controllers:
            # merge in the controllers in the model_manager/model_system portion of the project (if any)
            self._merge_controllers(config)
        if 'parent' in config:
            parent_config = self.get_run_configuration(config['parent'], merge_controllers=False)
            del config['parent']
            parent_config.merge(config)
            config = parent_config

        elif 'parent_old_format' in config:
            d = config['parent_old_format']
            parent_config = self._make_instance(d['Class_name'], d['Class_path'])
            del config['parent_old_format']
            parent_config.merge(config)
            config = parent_config

        config['project_name'] = project_name
        return config

    def get_estimation_configuration(self, model_name = None, model_group = None):
        """Extract an estimation configuration from this xml project and return it.
        If the configuration has an expression library, add
        that to the configuration under the key 'expression_library'
        If the model_name argument is given, also parse overriding
        configurations for that specific model."""
        # grab general configuration for estimations

        config = self.get_section('model_manager/estimation_config')
        # config = config_section['estimation_config']
        self._merge_controllers(config)
        self._insert_expression_library(config)

        if model_name is None:
            return config

        config['model_name'] = model_name
        config_node_path = "model_manager/models/model[@name='%s']/estimation_config" % model_name
        model_specific_overrides = self.get_section(config_node_path) or {}
        estimate_config = {}
        # If the user have specified a custom list of models to run before the estimation, then we
        # need to append the model to estimate as well or the modeling system will forget it...
        if 'models' in model_specific_overrides:
            if model_group is None:
                model_specific_overrides['models'].append({model_name: ["estimate"]})
            else:
                group_members = {'group_members': [{model_group:['estimate']}]}
                model_specific_overrides['models'].append({model_name: group_members})

        # look if any of the submodels have 'starting_values' set for any of the coefficient.
        path_to_specification = "model_manager/models/model[@name='%s']/specification" % model_name
        specification_node = self._find_node(path_to_specification)
        if specification_node is not None:
            variable_specs = [node for node in specification_node.findall('.//variable_spec') if
                              node.get('starting_value') and node.get('ignore') != 'True']
            # here we want something that looks like: {'starting_values': {'coeff-name': 34.2} }
            # or, if the value should be fixed, something like {'coeff-name': (34.2, True) }
            starting_values = {}
            for variable_node in variable_specs:
                coeff_name = variable_node.get('coefficient_name') or get_variable_name(variable_node)
                starting_value = float(variable_node.get('starting_value'))
                if variable_node.get('keep_fixed') == 'True':
                    starting_values[coeff_name] = (starting_value, False)
                else:
                    starting_values[coeff_name] = starting_value
            if starting_values:
                estimate_config = {'estimate_config': {'starting_values': starting_values}}

        # don't pass an empty dict into the 'config_changes_for_estimation' or the modeling system
        # will break
        if model_specific_overrides:
            config['config_changes_for_estimation'] = {model_name: model_specific_overrides}
        if estimate_config:
            if config['models_configuration'].get(model_name,{}).get('controller', {}).get('init',{}).get('arguments',{}):
                config['models_configuration'][model_name]['controller']['init']['arguments'].merge(estimate_config)
            else:
                # Hana (06/30/2011)
                # It should actually not go into 'config_changes_for_estimation' because it would overwrite existing estimate_config
                # But not sure under which circumstances the condition above would be not fulfilled.
                if not config.get('config_changes_for_estimation'):
                    config['config_changes_for_estimation'] = {model_name: estimate_config}
                else:
                    config['config_changes_for_estimation'].merge({model_name: estimate_config})
        return config

    def get_estimation_specification(self, model_name, model_group=None):
        """Get the estimation specification for the given model and return it as a dictionary."""
        # all_vars is the list of variables from the expression library
        all_vars = []
        lib_node = self._find_node('general/expression_library')
        for v in lib_node.iterchildren(tag=Element):
            var_name = get_variable_name(v)
            var_def = v.text
            # If the variable is defined as an expression, make an alias.
            # Otherwise it's a Python class.  If the name in the expression library
            # is the same as the variable short name, just use it as is; otherwise
            # also set up an alias.
            if v.get('source') == 'expression':
                add_alias = True
            else:
                n = VariableName(var_def)
                # don't need to add alias if it's the same as the name
                add_alias = n.get_short_name() != var_name
            if add_alias:
                all_vars.append('%s = %s' % (var_name, var_def))
            else:
                all_vars.append(var_def)
        # sort the list of variables to make it easier to test the results
        all_vars.sort()
        model_node = self._find_node('model_manager/models/model', model_name)
        # group_nodes is a dict where the keys are the groups and the values are a list of
        # submodel nodes in that group
        group_nodes = dict((node.get('name'), node.findall('submodel'))
                           for node in model_node.findall('specification/submodel_group'))
        # submodel nodes that are directly under the model are assumed to be ungrouped
        ungrouped_nodes = model_node.findall('specification/submodel')

        result = {}
        dataset_names = []

        # iterate over just the submodels in the given group (or over the ungrouped if no group is
        # provided
        submodel_nodes = ungrouped_nodes
        if model_group is not None:
            submodel_nodes = group_nodes[model_group]

        for submodel_node in submodel_nodes:
            submodel_id = int(submodel_node.get('submodel_id'))
            result[submodel_id] = {}
            # group by nests if there are any
            nest_nodes = submodel_node.findall('nest')
            if nest_nodes:
                result[submodel_id]['name'] = 'nest_id'
                nodes = nest_nodes
                res = {}
            else:
                nodes = [submodel_node]
            # group by equations if there are any, otherwise just give a list
            for node in nodes:
                equation_nodes = node.findall('equation')
                if equation_nodes:
                    submodel_equations = {}
                    for equation_node in equation_nodes:
                        equation_id = int(equation_node.get('equation_id'))
                        variable_list = self._convert_node_to_data(equation_node.find('variable_list'))
                        dataset_names += map(get_variable_dataset, only_no_comment(equation_node.find('variable_list')))
                        submodel_equations[equation_id] = variable_list
                    thisres = submodel_equations
                else:
                    thisres = self._convert_node_to_data(node.find('variable_list'))
                    dataset_names += map(get_variable_dataset, only_no_comment(node.find('variable_list')))
                if nest_nodes:
                    nest_id = int(node.get('nest_id'))
                    res[nest_id] = thisres
                else:
                    res = thisres
            if isinstance(res, dict):
                result[submodel_id].update(res)
            else:
                result[submodel_id] = res
                
        ## filter out variable definition we won't use - to allow variables of the same alias but for different dataset
        ## stop doing this if there are variables with unknown dataset_name
        if None in dataset_names or '' in dataset_names:
            result['_definition_'] = all_vars
        else:
            #result['_definition_'] = [v for v in all_vars for dataset_name in set(dataset_names) if VariableName(v).get_dataset_name()==dataset_name]
            # The line above was replaced by the loop below because dataset_name of an autogen class of an interaction dataset is None in VariableName.
            # Therefore all such variables are included in the definition.
            result['_definition_'] = []
            for v in all_vars:
                var_dataset_name = VariableName(v).get_dataset_name()
                if var_dataset_name is None:
                    result['_definition_'].append(v)
                else:
                    for dataset_name in set(dataset_names):
                        if var_dataset_name==dataset_name:
                            result['_definition_'].append(v)
                

        
        # model system expects the result to be categorized by the model_group if one is provided
        if model_group is not None:
            return {model_group: result}
        return result

    def save(self):
        """save this configuration in a file with the same name as the original"""
        self.save_as(self.full_filename)

    def save_as(self, filename = '', file_object = None):
        """
        save this configuration under a new name
        @param filename (str) filename to save under
        @param file_object (file) file object to save to (filename is ignored when this is not None)
        """
        self._indent(self.tree.getroot())
        if file_object is not None:
            self.tree.write(file_object, pretty_print = True)
        else:
            self.tree.write(str(filename), pretty_print = True)

    def find(self, path):
        """return the string encoding of the node referenced by 'path', or None if there is no such node"""
        n = self._find_node(path)
        if n is None:
            return n
        else:
            return tostring(n)
        
    def _init_first_writable_parent_file(self):
        """Stores the location of the first writable parent of the configuration file in self.first_writable_parent_file.
        Stores None if a configuration does NOT have a parent"""
        self.first_writable_parent_file = None
        parent_nodes = self.full_tree.getroot().findall('general/parent')
        for p in parent_nodes:
            first_parent_file = self._find_parent_file(p.text, self._get_default_dir())
            if first_parent_file:
                if os.access(first_parent_file, os.W_OK):
                    self.first_writable_parent_file = first_parent_file
                    return
        
    def get_first_writable_parent_file(self):
        return self.first_writable_parent_file

    def get_opus_data_path(self):
        """return the path to the opus_data directory.  This is found in the environment variable
        OPUS_DATA_PATH, or if that environment variable doesn't exist, as the contents of the
        environment variable OPUS_HOME followed by 'data' """
        from opus_core import paths
        return paths.OPUS_DATA_PATH

    def _initialize(self, elementtree, is_parent):
        self.tree = elementtree
        self.full_tree = copy.deepcopy(self.tree)
        full_root = self.full_tree.getroot()
        if full_root.tag != 'opus_project':
            raise ValueError, "malformed xml - expected to find a root element named 'opus_project'"

        # set the parser to this files xml version
        version_node = self.tree.getroot().find('xml_version')
        if version_node is not None:
            self.xml_version = XMLVersion(version_node.text)
        else:
            # files w/o specified version get optimistically regarded as up-to-date
            self.xml_version = XMLVersion(maximum_xml_version)
        # check that the version number is OK
        if self.xml_version < minimum_xml_version:
            raise XMLVersionException, ("XML version for this project file is less than the minimum required XML version.\n"
                + "  File name: %s \n  XML version found: %s  \n  minimum required: %s") % (self.full_filename, self.xml_version, minimum_xml_version)
        if self.xml_version > maximum_xml_version:
            raise XMLVersionException, ("XML version for this project file is greater than the maximum expected XML version.\n"
                + "(Likely fix: update your version of the Opus/UrbanSim code.)\n"
                + "  File name: %s \n  XML version found: %s \n  maximum expected: %s") % (self.full_filename, self.xml_version, maximum_xml_version)

        # The merging of inherited trees is done in two steps.
        # The first step is to merge inherited trees into one big tree (self.inherited_tree)
        # and the second step is to merge that tree into the configurations full_tree.
        # this is done so that we always have a copy of all the inherited values that we can
        # use to restore deleted or renamed nodes.

        # step 1 - collect and merge all parent trees
        # we need to init inherited_configs lazily to avoid infinite recursion
        inherited_configs = None
        for root_of_a_parent in self._get_parent_trees():
            if inherited_configs is None:
                inherited_configs = XMLConfiguration()
            inherited_root = inherited_configs.full_tree.getroot()
            XMLConfiguration._merge_nodes(root_of_a_parent, inherited_root)
        # step 2 - merge any inherited trees into this config
        if inherited_configs:
            self.inherited_tree = copy.deepcopy(inherited_configs.full_tree.getroot())
            XMLConfiguration._merge_nodes(inherited_configs.full_tree.getroot(), self.full_tree.getroot())

        # keep track of where we inherited nodes
        if is_parent:
            for n in full_root.getiterator(tag=Element):
                if n.get('inherited') is None:
                    n.set('inherited', self.name)
        # Parent map... can be used for working back up the XML tree
        self.parent_map = dict((c, p) for p in self.full_tree.getiterator() for c in p)
        
        self._init_first_writable_parent_file()

    def _indent(self, element, level=0):
        '''
        Indents the (internal) text representation for an Element.
        This is used before saving to disk to generate nicer looking XML files.
        (this code is based on code from http://effbot.org/zone/element-lib.htm)
        '''
        i = "\n" + level * "  "
        if len(element):
            if not element.text or not element.text.strip():
                element.text = i + "  "
            if not element.tail or not element.tail.strip():
                element.tail = i
            child_element = None
            for child_element in element:
                self._indent(child_element, level+1)
            if not child_element.tail or not child_element.tail.strip():
                child_element.tail = i
        else:
            if not element.tail or not element.tail.strip():
                element.tail = i

    def _find_node(self, path, name = None, get_all = False):
        '''
        get one or more nodes from the xml tree by looking up the path.
        @param path xml path to the node to return. The root is returned if path is an empty string.
        @param name optional argument to filter element(s) by name.
        @param get_all if True, all the matching element are returned, not just the first one.
        '''

        if path == '':
            return self.full_tree.getroot()

        if name is None:
            if get_all:
                return self.full_tree.getroot().findall(path)
            else:
                return self.full_tree.getroot().find(path)

        matching_nodes = [node for node in self.full_tree.getroot().findall(path) if
                          node.get('name').strip() == name.strip()]
        if len(matching_nodes) < 1:
            return None
        # return all or the first match
        return matching_nodes if get_all else matching_nodes[0]

    def _get_default_dir(self):
        return os.path.split(self.full_filename)[0]

    def _get_parent_trees(self):
        default_dir = self._get_default_dir()
        parent_nodes = self.full_tree.getroot().findall('general/parent')
        parent_trees = []
        for p in parent_nodes:
            x = XMLConfiguration(p.text, default_directory=default_dir, is_parent=True)
            parent_trees.append(x.full_tree.getroot())

            # TODO CK: maybe figure out a place where it makes more sense to
            # check for version switching warnings. Placed it here because this
            # is the only place I could find where we have access to the parent
            # configuration objects

            # merge any warnings from inherited XML configurations
            if x.version_warning_message:
                self.version_warning_message = self.version_warning_message + \
                    x.version_warning_message + '\n'
            # if necessary, add a version inconsistent warning
            if x.xml_version != self.xml_version:
                self.version_warning_message = (self.version_warning_message +
                'version "%s" in  %s is different from version "%s" in %s'
                %(x.xml_version, os.path.basename(x.full_filename),
                  self.xml_version, os.path.basename(self.full_filename)))
        return parent_trees

    @staticmethod
    def _merge_nodes(parent_node, local_node):
        # the merging assumes that the two nodes have the same node_path, no check is performed
        # merging is done by copying all attributes from the parent_node if they don't already
        # exist in the local node. The attribute 'inherited' is a special case and is never copied.
        # All child nodes of the parent_node with the same node id as child nodes of local_node are
        # also merged. Other child nodes are added to the local_node.
        # print 'merging nodes (p>c): %s -> %s' %(parent_node, local_node)
        if local_node.get('inherit_parent_values') == 'False': # or \
            #parent_node.get('inherit_parent_values') == 'False':
            ## allow parent to specify nodes that are not supposed to be inherited
            return
        for name, value in parent_node.items():
            if name != 'inherited' and not name in local_node.attrib:
                local_node.set(name, value)
        # pair up nodes with their id's
        parent_child_nodes = dict((node_identity_string(n), n) for n in parent_node.getchildren())
        local_child_nodes = dict((node_identity_string(n), n) for n in local_node.getchildren())
        # decide what to do with each child node of the parent tree
        node_index = 0
        for n in parent_node.getchildren():
            id_ = node_identity_string(n)
            parent_child_node = parent_child_nodes[id_]
            if id_ in local_child_nodes:
                # the local node already has this node, merge the two
                local_child_node = local_child_nodes[id_]
                XMLConfiguration._merge_nodes(parent_child_node, local_child_node)
                # default next position to insert is after this node
                node_index = local_node.getchildren().index(local_child_node)+1
            else:
                # this node (and its subtree) doesn't exist under the local node. We want to insert
                # it in a sensible place.
                # respect any sibling that have the followers attribute set when inserting the node
                nodes_with_followers = [n for n in local_node.getchildren() if n.get('followers')]
                for node_with_followers in nodes_with_followers:
                    followers_list = node_with_followers.get('followers').split(',')
                    if parent_child_node.tag in followers_list:
                        # place after the node with the followers list (unless it will already be placed after)
                        after = 1 + local_node.getchildren().index(node_with_followers)
                        if node_index < after:
                            node_index = after
                local_node.insert(node_index, parent_child_node)
                node_index = node_index+1

    def _clean_tree(self, etree):
        # Remove from etree any nodes with the 'temporary' or 'inherited' attribute.
        # Use a counter rather than to handle the problem of deleting a node while iterating
        i = 0
        while i<len(etree):
            e = etree[i]
            if e.get('temporary')=='True' or e.get('inherited') is not None:
                del etree[i]
            else:
                self._clean_tree(e)
                i = i+1

    def _set_followers(self, tree, parent_trees, path):
        # Recursively traverse tree, setting the 'followers' attribute on any node
        # that needs it.  A node n should have a 'followers' attribute if it is new in
        # 'tree' and doesn't occur in any parent.  If so, 'followers' should be a
        # comma-separated list of names of inherited nodes that follow n.  (This is used
        # when merging in inherited nodes to put them in the right place.)
        children = tree.getchildren()
        for i, n in enumerate(children):
            if is_comment(n):
                continue
            if n.get('inherited') is None:
                is_new = True
                if path== '':
                    extended_path = n.tag
                else:
                    extended_path = path + '/' + n.tag
                # check if n occurs in any parent
                for p in parent_trees:
                    if p.find(extended_path) is not None:
                        is_new = False
                        break
                if is_new:
                    followers = map(lambda x: x.tag, filter(lambda y: y.get('inherited') is not None, children[i+1:]))
                    if len(followers)>0:
                        s = ','.join(followers)
                        n.set('followers', s)
                self._set_followers(n, parent_trees, extended_path)

    def _merge_controllers(self, config):
        '''
        The model system looks for model configurations in:
            config['model_configuration']['controller'] = {<model config>}
        which is different from the XML structure:
            (model_manager/models/{model_config}
        So we need to move the information around a little.
        It also add dependencies derived from the model structure.
        '''
        # get all model configurations (from model/structure), indexed by name
        controller_configs = {}
        for model_node in self._find_node('model_manager/models/model', get_all = True):
            model_name = model_node.get('name')
            model_config = self._convert_model_to_dict(model_node)
            controller_configs[model_name] = {'controller': model_config}
            model_dependencies = self.model_dependencies(model_name)
            if model_dependencies:
                controller_configs[model_name]['controller']['_model_structure_dependencies_'] = model_dependencies
        # the modeling system can get confused if there's an empty controller config present
        if controller_configs:
            config['models_configuration'] = controller_configs          

    def _node_to_config(self, node):
        config = {}
        for child in node.iterchildren(tag=Element):
            self._add_to_dict(child, config)
        return config

    def _add_to_dict(self, node, result_dict):
        # Add the information in 'node' to 'result_dict'.  The way this is done depends on the node type and the
        # parser_action (if present).  The normal case is that 'node' is an element node representing a key-value pair
        # to be added to 'result_dict'.  But there are a couple of special cases.
        # If the type is 'category' or 'category_with_special_keys' add the children to result_dict.
        # (See the comment for _convert_dictionary_with_special_keys_to_data for details on how that type is handled.)
        # If it's an 'include', find the referenced node and add its children to result_dict.
        action = node.get('parser_action', '')
        if action=='include':
            included = self._find_node(node.text)
            for child in included.iterchildren(tag=Element):
                self._add_to_dict(child, result_dict)
        # some nodes should not end up in the dict
        elif action in ['only_for_includes', 'skip']:
            pass
        else:
            # respect nodes with explicit preference for key names
            if 'config_name' in node.attrib:
                key = node.get('config_name')
            elif node.get('name'):
                key = node.get('name')
            else:
                key = node.tag
            if action == 'convert_key_to_integer':
                key = int(key)
            data = self._convert_node_to_data(node)
            type_name = node.get('type')
            if type_name=='category' or type_name=='category_with_special_keys':
                result_dict.update(data)
            else:
                result_dict[key] = data

    def _convert_node_to_data(self, node):
        # convert the information under node into the appropriate Python datatype.
        # To do this, branch on the node's type attribute.  For some kinds of data,
        # return None if the node should be skipped.
        type_name = node.get('type')
        if type_name=='integer':
            return self._convert_string_to_data(node, int)
        elif type_name=='float':
            return self._convert_string_to_data(node, float)
        #TODO Remove the support for "quoted_string" before 4.3 release.
        elif type_name in ['string', 'password', 'variable_definition', 'path', 'quoted_string']:
            if type_name == 'quoted_string':
                node.attrib['parser_action'] = 'quote_string'
            return self._convert_string_to_data(node, str)
        elif type_name=='scenario_name':
            return node.text
        elif type_name=='unicode':
            return self._convert_string_to_data(node, unicode)
        elif type_name=='selectable_list':
            return self._convert_list_to_data(node)
        elif type_name=='variable_list':
            return self._convert_variable_list_to_data(node)
        elif type_name=='tuple':
            return self._convert_tuple_to_data(node)
        elif type_name=='list':
            return eval(node.text)
        elif type_name=='boolean':
            return eval(node.text)
        elif type_name=='file':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='directory':
            return self._convert_file_or_directory_to_data(node)
        elif type_name=='array':
            # the data should be a string such as '[100, 300]'
            # use eval to turn this into a list, and then turn it into a numpy array
            return array(eval(node.text))
        elif type_name in ['dictionary', 'category', 'submodel', 'submodel_group',
                           'model_system', 'configuration','model_estimation',
                           'submodel_equation', 'scenario']:
            return self._convert_dictionary_to_data(node)
        elif type_name in ['model_template', 'estimation_template']:
            return None
        elif type_name == 'model':
            return self._convert_model_to_dict(node)
        elif type_name=='category_with_special_keys':
            return self._convert_dictionary_with_special_keys_to_data(node)
        elif type_name=='class':
            return self._convert_class_to_data(node)
        elif type_name=='database_library':
            return ''
        elif type_name=='db_connection':
            return ''
        elif type_name=='db_connection_hook':
            return node.text
        elif type_name in ['selectable', 'model_choice']:
            return self._convert_selectable_to_data(node)
#        elif type_name=='model_choice':
#            return self._convert_custom_type_to_data(node, "Skip")
#        elif type_name=='table':
#            return self._convert_custom_type_to_data(node, "Skip")
#        elif type_name=='dataset':
#            return self._convert_custom_type_to_data(node, "Skip")
#        elif type_name=='variable':
#            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='python_code':
            return eval(node.text)
        else:
            raise ValueError, ('unknown type: %s (node: %s[name=%s])'
                               % (type_name, node.tag, node.get('name')))

    def _make_instance(self, class_name, path, keyword_args = {}):
        # return an instance of the class named class_name.  path is the path to import it.
        if path=='':
            cls = eval('%s()' % class_name)
        else:
            # use the fully-qualified class name rather than a 'from pkg import classname'
            # to avoid cluttering up the local name space
            exec('import %s' % path)
            cls = eval('%s.%s' % (path, class_name))
        inst = cls.__new__(cls)
        inst.__init__(**keyword_args)
        return inst

    def _convert_string_to_data(self, node, func):
        convert_blank_to_none = node.get('convert_blank_to_none') == 'True'
        quote_string = node.get('parser_action') == 'quote_string'
        # not giving any strings means giving empty strings. To explicitly give None, set the
        # attribute convert_empty_string_to_none to 'True'.
        node_text = node.text

        if node_text is None:
            node_text = ''

        if convert_blank_to_none:
            if node_text in ['', 'None']:
                return None

        resulting_string = func(node_text)

        # ensure the string is quoted (single quotes) if requested to do so
        if quote_string:
            resulting_string = resulting_string.replace('"', "'").replace("'", '')
            resulting_string = "'%s'" % resulting_string
        return resulting_string

    def _convert_list_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node.iterchildren(tag=Element))
        result_list = filter(lambda n: n is not None, r)
        if node.get('parser_action', '') == 'list_to_dictionary':
            result_dict = {}
            for x in result_list:
                if isinstance(x, str):
                    result_dict[x] = {}
                else:
                    # x should be a dictionary with one entry
                    result_dict.update(x)
            return result_dict
        else:
            return result_list

    def _convert_variable_list_to_data(self, variable_list_node):
        '''
        Convert a list of variable names to Python data.
        This function is external because it's functionality is used in both the GUI and in the
        XMLConfiguration class.

        Each variable in the variable list is given as a <variable_spec> node.
        '''
        # tiny helper for returning coefficient name, variable name tuples or just variable name
        def name_or_tuple(var_node):
            name = get_variable_name(var_node)
            coeff_name = var_node.get('coefficient_name')
            fixed_value = var_node.get('fixed_value')
            if fixed_value and not coeff_name:
                coeff_name = name
            if fixed_value:
                return (name, coeff_name, float(fixed_value))
            if coeff_name:
                return (name, coeff_name)
            return name
        f = lambda x: x.get('ignore') != 'True'
        return map(name_or_tuple, filter(f, variable_list_node.iterchildren(tag=Element)))

    def _convert_tuple_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node.iterchildren(tag=Element))
        return tuple(r)

    def _convert_file_or_directory_to_data(self, node):
        if node.get('parser_action', '')=='prefix_with_opus_data_path':
            return os.path.join(self.get_opus_data_path(), node.text)
        elif node.get('parser_action', '')=='prefix_with_opus_core':
            return os.path.join(directory_path_from_opus_path('opus_core'), node.text)
        else:
            return node.text

    def _convert_dictionary_to_data(self, node):
        result_dict = {}
        for child in node.iterchildren(tag=Element):
            self._add_to_dict(child, result_dict)
        return result_dict

    def _convert_model_to_dict(self, node):
        '''translate from xml structure to dictionary configuration.'''
        structure_node = node.find('structure')
        if structure_node is None:
            structure_node = Element('zzyxy')
        model_dict = {}
        for subnode in structure_node.iterchildren(tag=Element):
            # append 'arguments' to some nodes
            if subnode.tag in ['init', 'run', 'prepare_for_run',
                               'estimate', 'prepare_for_estimate']:
                subnode_struct = {'arguments':{}}
                # everything but 'name' and 'output' should be under arguments
                for arg_node in subnode.iterchildren(tag=Element):
                    if not arg_node.tag in ['name', 'output']:
                        self._add_to_dict(arg_node, subnode_struct['arguments'])
                    else:
                        self._add_to_dict(arg_node, subnode_struct)
                model_dict[subnode.tag] = subnode_struct
            # for 'import', the model system wants a dict like {'python.module': 'ClassName'}
            elif subnode.tag == 'import':
                model_module = subnode.find("class_module").text
                model_classname = subnode.find("class_name").text
                model_dict['import'] = {model_module: model_classname}
            else: # just put it in the dict
                model_dict[subnode.tag] = self._convert_node_to_data(subnode)
                
        dependencies = node.find('dependencies')
        if dependencies is not None:
            self._add_to_dict(dependencies, model_dict)
        return model_dict

    def _convert_dictionary_with_special_keys_to_data(self, node):
        # Node should be converted to a dictionary of dictionaries, typically with keys in the top-level dictionary
        # that are integers.  Since in xml tags can't be integers, this is handled with this special type.  The
        # elements under the node are parsed into dictionaries (their tags don't matter).  The node must have an
        # attribute 'key_name'.  The key name is used to find the key for each element in the top-level dictionary,
        # and is deleted from the second-level dictionary.
        # See the unit tests for an example - that may make it clearer what this does.
        key_name = node.get('key_name')
        key_value = node.get('key_value', 'UnlIkElY_nAmE')
        result = {}
        for child in node.iterchildren(tag=Element):
            d = self._convert_node_to_data(child)
            k = d[key_name]
            del d[key_name]
            if d.has_key(key_value):
                v = d[key_value]
                del d[key_value]
                result[k] = v
            else:
                result[k] = d
        return result

    def _convert_class_to_data(self, node):
        '''
        This example illustrates how classes are specified and what the returning value is:

        From:

            <some_node type="class">
             <class_name>MyClass</class_name>
             <class_module>module.in.python.path</class_module>
             <argument name="a_string" type="string">String value</argument>
             <argument name="an_int" type="integer">9</argument>
            </some_node>

        To:
            dict['some_node'] = module.in.python.path.MyClass(a_string = "String value", an_int = 9)

        The return value can also be the result of executing the method 'execute()' on the
        instantiated class. This happens if the 'parser_action' attribute of some_node is set to
        'execute'. For example;
        if the above XML had <some_node type="class" parser_action="execute"> as a root node, then
        the result would be:

            instance = module.in.python.path.MyClass(a_string = "String value", an_int = 9)
            dict['some_node'] = instance.execute()

        '''
        class_name = node.find('class_name').text
        class_module = node.find('class_module').text
        keyw_arguments = {}
        for argument_node in node.findall('argument'):
            self._add_to_dict(argument_node, keyw_arguments)
        instance = self._make_instance(class_name, class_module, keyw_arguments)

        if node.get('parser_action', '')=='execute':
            return instance.execute()
        else:
            return instance

    def _convert_selectable_to_data(self, node):
        ''' Convert a selectable item to data.
        A node is considered selected if its text-value is set to 'True', otherwise return None.
        If the node has child nodes, it's returned as a dictionary. If it's a leaf one either the
        nodes 'name' attribute or the attribute 'return_value' is returned ('return_value' has
        precedence).

        Examples:
        <selectable name='guppy'>True</selectable> = "guppy"
        <selectable name='squid' return_value="guppy">True</selectable> = "guppy"
        <selectable name="squid">                     |
         <integer name='guppy'>4</integer>            |= {"squid": {"guppy": 4}}
        </selectable>                                 |
        '''
        if node.text.strip() != 'True':
            return None
        result_name = node.get('return_value') or node.get('name')

        subdict = {}
        for child_node in node.iterchildren(tag=Element):
            self._add_to_dict(child_node, subdict)
        return {result_name: subdict} if subdict else result_name

    def _convert_custom_type_to_data(self, node, skip):
        # skip is a string that is the value when this node should be skipped
        if node.text==skip:
            return None
        name = node.tag
        subdict = {}
        for child in node.iterchildren(tag=Element):
            self._add_to_dict(child, subdict)
        return {name: subdict} if subdict else name

    def _insert_expression_library(self, config):
        # insert the expression library into config, if it isn't empty
        lib = self.get_expression_library()
        if len(lib) > 0:
            config['expression_library'] = lib

    def model_dependencies(self, model_name=None):
        """Find all nodes in 'model' section that have model_dependency_type defined.
        Return a dictionary with keys being dependency types and each value being a list 
        of dependencies of that type. If model_name is None, all models in the 'models' section
        are considered.
        """
        def get_dependencies(node):
            children = node.getchildren()
            for child in children:
                # We now can have both children...
                get_dependencies(child)
                
                # and dependencies due to comments.
                dependency_type = child.get('model_dependency_type')
                if dependency_type is None:
                    continue
                if dependency_type not in result.keys():
                    result[dependency_type] = []
                if child.text not in result[dependency_type] and child.text is not None:
                    result[dependency_type].append(child.text)
                
        result = {}
        if model_name is None:
            model_nodes = self._find_node('model_manager/models/model', get_all = True)
        else:
            model_nodes = [self._find_node('model_manager/models/model', model_name)]
        for model_node in model_nodes:
            get_dependencies(model_node)
        return result
                

from numpy import ma
import StringIO
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.variables.variable_factory import VariableFactory

class XMLConfigurationTests(opus_unittest.OpusTestCase):

    def setUp(self):
        # find the directory containing the test xml configurations
        opus_core_dir = __import__('opus_core').__path__[0]
        self.test_configs = os.path.join(opus_core_dir, 'configurations', 'test_configurations')

    def _nodes_by_name(self, node, node_tag = ''):
        list_of_nodes = node.findall(node_tag) if node_tag else node.getchildren()
        return dict((node.get('name'), node) for node in list_of_nodes)

    def assertElementsEqual(self, element_one, element_two, include_tree = False):
        '''
        Test two elements for equality.
        Two elements are considered equal if they have the same tag, and the same
        attributes with the same values. Order of the attributes does not matter.
        '''
        assertion_text = '%s (%s) != %s (%s)' % \
                       (element_one, str(element_one.attrib), element_two, str(element_two.attrib))
        if not element_one.tag == element_two.tag:
            raise AssertionError(assertion_text)
        e1_attribs = element_one.attrib.keys()
        e2_attribs = element_two.attrib.keys()
        e1_attribs.sort()
        e2_attribs.sort()
        if e1_attribs != e2_attribs:
            raise AssertionError('%s:%s' %(e1_attribs, e2_attribs)) # assertion_text)
        for attrib in e1_attribs:
            if element_one.attrib[attrib] != element_two.attrib[attrib]:
                raise AssertionError(assertion_text)
        e1txt = element_one.text or ''
        e2txt = element_two.text or ''
        if e1txt.strip() != e2txt.strip():
            raise AssertionError(assertion_text)
        if include_tree:
            for c1, c2 in zip(element_one.getchildren(), element_two.getchildren()):
                self.assertElementsEqual(c1, c2, include_tree)

    def test_types(self):
        f = os.path.join(self.test_configs, 'manytypes.xml')
        config = XMLConfiguration(f).get_section('test_section')
        self.assertEqual(config,
                         {'description': 'a test configuration',
                          'quotedthing': r"'test\test'",
                          'quotedthing2': r"'test\test'",
                          'quotedthing3': r"'test\test'",
                          'empty1': '',
                          'empty2': None,
                          'the selectables': ['res1', 'res2', {'dict': {'five': 5, 'string': 'string'}}],
                          'emptypassword': None,
                          'year': 1980,
                          'mybool': True,
                          'ten': 10.0,
                          'emptyint': None,
                          'emptyfloat': None,
                          'years': (1980, 1981),
                          'list_test': [10, 20, 30],
                          'vars': ['grid_variable', 'constant', ('constant', 'constant_coeff'),
                                   ('var_with_coeff', 'the_coeff')],
                          'dicttest': {'str1': 'squid', 'str2': 'clam'},
                          'models_to_run': ['real_estate_price_model'],
                          'mytables': ['gridcells', 'jobs'],
                          'mydatasets': ['gridcell', 'job']
                          })

    def test_whitespace_and_comments(self):
        f = os.path.join(self.test_configs, 'whitespace.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config, {'project_name':'test_project',
                          'description': 'a test configuration'})

    def test_str_and_unicode(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'strings.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        for k in config.keys():
            self.assert_(type(k) is str)
        self.assert_(type(config['s']) is str)
        self.assert_(type(config['u']) is unicode)

    def test_array(self):
        # check that the keys in the config dictionary are str, and that
        # the str and unicode tags are working correctly
        f = os.path.join(self.test_configs, 'array.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        should_be = array([100, 300])
        self.assert_(ma.allclose(config['arraytest'], should_be, rtol=1e-6))

    def test_files_directories(self):
        # if the OPUS_HOME environment variable isn't set, temporarily set it so that
        # the prefix_with_opus_data_path parser command can be tested
        if 'OPUS_HOME' not in os.environ:
            os.environ['OPUS_HOME'] = os.path.expanduser('~/opus')
        f = os.path.join(self.test_configs, 'files_directories.xml')
        x = XMLConfiguration(f)
        config = x.get_run_configuration('test_scenario')
        prefix = x.get_opus_data_path()
        self.assertEqual(config, {'project_name':'test_project',
                                  'file1': 'testfile',
                                  'file2': os.path.join(prefix, 'testfile'),
                                  'dir1': 'testdir',
                                  'dir2': os.path.join(prefix, 'testdir')})

    def test_scenario_inheritance(self):
        # test inheritance of scenarios with a chain of xml configurations
        f = os.path.join(self.test_configs, 'child_scenarios.xml')
        config = XMLConfiguration(f).get_run_configuration('child_scenario')
        self.assertEqual(config,
            {'project_name':'test_project','description': 'this is the child', 'year': 2000, 'modelname': 'widgetmodel'})

    def test_scenario_inheritance_external_parent(self):
        # test inheritance of scenarios with an external_parent (one with original name, one renamed)
        f = os.path.join(self.test_configs, 'grandchild_scenario_external_parent.xml')
        config1 = XMLConfiguration(f).get_run_configuration('grandchild')
        self.assertEqual(config1,
            {'project_name':'test_project','description': 'this is the grandchild', 'year': 2000, 'modelname': 'widgetmodel'})

    def test_old_config_inheritance(self):
        # test inheriting from an old-style configuration
        # (backward compatibility functionality - may be removed later)
        f = os.path.join(self.test_configs, 'child_scenario_oldparent.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        # 'years' is overridden in the child
        self.assertEqual(config['years'], (1980, 1981))
        # 'squidcount' is new in the child
        self.assertEqual(config['squidcount'], 12)
        # 'models' is inherited
        self.assert_('models' in config)
        self.assert_('random_nonexistant_key' not in config)

    def test_categories(self):
        f = os.path.join(self.test_configs, 'categories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config,
                         {'project_name':'test_project',
                          'description': 'category test',
                          'real_name': 'config name test',
                          'precache': True,
                          'chunksize': 12,
                          'years': (1980, 1981),
                          'bool2': False,
                          'int2': 13})

    def test_list_to_dict(self):
        f = os.path.join(self.test_configs, 'list_to_dict.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config,
                         {'project_name':'test_project',
                          'datasets_to_preload': {'job': {}, 'gridcell': {'nchunks': 4}}})

    def test_include(self):
        f = os.path.join(self.test_configs, 'include_test.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        self.assertEqual(config,
                         {'project_name':'test_project',
                          'description': 'a test scenario',
                          'firstyear': 2000,
                          'lastyear': 2020,
                          'x': 10,
                          'y': 20,
                          'morestuff': {'x': 10, 'y': 20}})

    def test_class_element(self):
        # test a configuration element that is a specified class
        f = os.path.join(self.test_configs, 'database_configuration.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['scenario_database_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')

    def test_class_element_with_categories(self):
        # like test_class_element, but with an additional layer of categorization in the xml
        f = os.path.join(self.test_configs, 'database_configuration_with_categories.xml')
        config = XMLConfiguration(f).get_run_configuration('test_scenario')
        db_config = config['scenario_database_configuration']
        self.assertEqual(db_config.protocol, 'mysql')
        self.assertEqual(db_config.host_name, 'bigserver')
        self.assertEqual(db_config.user_name, 'fred')
        self.assertEqual(db_config.password, 'secret')
        self.assertEqual(db_config.database_name, 'river_city_baseyear')

    def test_get_section(self):
        f = os.path.join(self.test_configs, 'parent1.xml')
        config = XMLConfiguration(f).get_section('general/expression_library')
        should_be = {
          'ln_cost': 'ln(psrc.parcel.cost)',
          'existing_units': 'urbansim_parcel.parcel.existing_units'}
        self.assertEqual(config, should_be)

    def test_get_section_of_child(self):
        f = os.path.join(self.test_configs, 'child1.xml')
        config = XMLConfiguration(f).get_section('general/expression_library')
        should_be = {
          'ln_cost': 'ln(psrc.parcel.cost)+10',
          'existing_units': 'urbansim_parcel.parcel.existing_units',
          'tax': 'urbansim_parcel.parcel.tax'}
        self.assertEqual(config, should_be)

    def test_inherited_nodes(self):
        # make sure that inherited attributes are tagged as 'inherited'
        f = os.path.join(self.test_configs, 'child1.xml')
        expression_library_node = XMLConfiguration(f).full_tree.find('general/expression_library')
        variable_nodes = self._nodes_by_name(expression_library_node, 'variable')
        # the ln_cost variable is redefined in child1, so it shouldn't have the 'inherited' attribute
        ln_cost_node = variable_nodes['ln_cost']
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is new, so also shouldn't have the 'inherited' attribute
        tax_node = variable_nodes['tax']
        self.assertEqual(tax_node.get('inherited'), None)
        # the existing_units variable is inherited and not overridden, so it should have 'inherited' set to the name of the parent
        existing_units_node = variable_nodes['existing_units']
        self.assertEqual(existing_units_node.get('inherited'), 'parent1')

    def test_inherited_tree(self):
        f = os.path.join(self.test_configs, 'child1.xml')
        xc = XMLConfiguration(f)
        # the ln_cost variable is redefined in child1, so it should be in inherited_tree and
        # have a different value than the local one
        ln_cost_in_parent = xc.inherited_tree.find('general/expression_library/variable[@name="ln_cost"]')
        ln_cost_local = xc.full_tree.find('general/expression_library/variable[@name="ln_cost"]')
        self.assertTrue(ln_cost_in_parent is not None)
        self.assertNotEqual(ln_cost_in_parent, ln_cost_local)
        # the tax variable is new, so also shouldn't be in inherited
        tax_node = xc.inherited_tree.find('general/expression_library/variable[@name="tax"]')
        self.assertEqual(tax_node, None)
        # the existing_units variable is inherited and not overriddenm should be same in
        # inherited_tree and local
        existing_units_parent = xc.inherited_tree.find('general/expression_library/variable[@name="existing_units"]')
        existing_units_local = xc.full_tree.find('general/expression_library/variable[@name="existing_units"]')
        self.assertTrue(existing_units_parent is not None)
        self.assertElementsEqual(existing_units_parent, existing_units_local)

    def test_grandchild_inherited_nodes(self):
        # test two levels of inheritance, with multiple inheritance as well
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        expression_library_node = XMLConfiguration(f).full_tree.find('general/expression_library')
        variable_nodes = self._nodes_by_name(expression_library_node, 'variable')
        # the ln_cost variable is redefined in grandchild, so it shouldn't have the 'inherited' attribute
        ln_cost_node = variable_nodes['ln_cost']
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is inherited from child1 (there is also a definition in child2 but that
        # shouldn't be used)
        tax_node = variable_nodes['tax']
        self.assertEqual(tax_node.get('inherited'), 'child1')
        # the extratax variable is inherited from child2
        extratax_node = variable_nodes['extratax']
        self.assertEqual(extratax_node.get('inherited'), 'child2')
        # the existing_units variable is inherited from parent1
        existing_units_node = variable_nodes['existing_units']
        self.assertEqual(existing_units_node.get('inherited'), 'parent1')

    def test_inherited_attributes(self):
        # make sure that inherited attributes are overridden properly, and otherwise passed through if not overridden
        path = 'general/test_node'
        f1 = os.path.join(self.test_configs, 'parent1.xml')
        n1 = XMLConfiguration(f1).full_tree.find(path)
        self.assertEqual(n1.get('test_attribute'), 'parent1_value')
        self.assertEqual(n1.get('oceanic_attribute'), 'squid')
        f2 = os.path.join(self.test_configs, 'child1.xml')
        n2 = XMLConfiguration(f2).full_tree.find(path)
        self.assertEqual(n2.get('test_attribute'), 'child1_value')
        self.assertEqual(n2.get('oceanic_attribute'), 'squid')
        f3 = os.path.join(self.test_configs, 'child2.xml')
        n3 = XMLConfiguration(f3).full_tree.find(path)
        self.assertEqual(n3.get('test_attribute'), 'parent1_value')
        self.assertEqual(n3.get('oceanic_attribute'), 'squid')
        f4 = os.path.join(self.test_configs, 'grandchild1.xml')
        n4 = XMLConfiguration(f4).full_tree.find(path)
        self.assertEqual(n4.get('test_attribute'), 'child1_value')
        self.assertEqual(n4.get('oceanic_attribute'), 'squid')
        
    def test_inherited_node_order(self):
        # there was a bug with the order of nodes getting flipped when overriding one of two nodes -- 
        # test this by getting the years_to_run node and turning it into a tuple
        f1 = os.path.join(self.test_configs, 'parent1.xml')
        config = XMLConfiguration(f1).get_section('general')
        self.assertEqual(config['years_to_run'], (1981, 1984))
        f2 = os.path.join(self.test_configs, 'child1.xml')
        config = XMLConfiguration(f2).get_section('general')
        self.assertEqual(config['years_to_run'], (1981, 2000))

    def test_find(self):
        # CK: disabling this for a while -- it's unreliable to test string representations
        # as the arguments can appear in an arbitrary order

        # test the 'find' method on inherited and non-inherited nodes
        f = os.path.join(self.test_configs, 'child1.xml')
        config = XMLConfiguration(f)
        ln_cost_str = fromstring(config.find('general/expression_library/variable[@name="ln_cost"]'))
        # should_be = '<ln_cost dataset="parcel" source="expression" type="variable_definition" use="model variable">ln(psrc.parcel.cost)+10</ln_cost>'
        should_be = fromstring('<variable '
                               'name="ln_cost" '
                               'type="variable_definition" '
                               'dataset="parcel" '
                               'use="model variable" '
                               'source="expression">'
                               'ln(psrc.parcel.cost)+10'
                               '</variable>')
        self.assertElementsEqual(ln_cost_str, should_be, include_tree=True)
        existing_units = fromstring(config.find('general/expression_library/variable[@name="existing_units"]'))
        # expected = '<existing_units dataset="parcel" source="Python class" type="variable_definition" use="model variable">urbansim_parcel.parcel.existing_units</existing_units>'
        expected = fromstring('<variable '
                              'name="existing_units" '
                              'inherited="parent1" '
                              'type="variable_definition" '
                              'dataset="parcel" '
                              'use="model variable" '
                              'source="Python class">'
                              'urbansim_parcel.parcel.existing_units'
                              '</variable>')
        self.assertElementsEqual(existing_units, expected, include_tree=True)
        squid_str = config.find('model_manager/estimation/squid')
        self.assertEqual(squid_str, None)

    def test_get_controller(self):
        # test getting a run specification that includes a controller in the xml
        f = os.path.join(self.test_configs, 'controller_test.xml')
        xml_config = XMLConfiguration(f)
        config = xml_config.get_run_configuration('baseline')
        should_be = { 'project_name':'test_project', 'models_configuration':
                    {'real_estate_price_model': {'controller': {'prepare_for_run':
                    { 'name': 'prepare_for_run', 'arguments':
                    {'specification_storage': 'base_cache_storage',
                     'specification_table': 'real_estate_price_model_specification'
                    }}}}}}
        self.assertEqual(config, should_be)

    def test_travel_model_config(self):
        # test whether the travel model section of a run configuration is being set correctly
        # this also tests the 'category_with_special_keys' type
        f = os.path.join(self.test_configs, 'travel_model.xml')
        config = XMLConfiguration(f).get_run_configuration('child_scenario')
        should_be = {'project_name': 'test_project', 'travel_model_configuration':
            {'travel_model_base_directory': 'base3',
             'emme2_batch_file_name': 'QUICKRUN.bat',
              2000: {'bank': ['2000_06'], 'emme2_batch_file_name': None}}}
        self.assertEqual(config, should_be)

    def test_get_estimation_specification(self):
        # test getting the estimation specification.  This also tests the expression library, which contains an expression
        # for ln_cost and a variable defined as a Python class.  In the _definition_ entry in the dictionary, we include an alias
        # if the name of the expression (a Python class reference in this case) is different from the variable name, as in
        # the bsqft variable.
        f = os.path.join(self.test_configs, 'estimate.xml')
        config = XMLConfiguration(f).get_estimation_specification('real_estate_price_model')
        should_be = {'_definition_': ['bsqft = urbansim_parcel.parcel.building_sqft', 'ln_cost = ln(psrc.parcel.cost)', 'urbansim_parcel.parcel.existing_units'],
          24: ['ln_cost', 'existing_units', 'bsqft'],
          25: ['existing_units', ('ln_cost', 'cost'), ('bsqft', 'bsqft', 10.0)]}
        self.assertEqual(config, should_be)

    def test_get_estimation_specification_with_equation(self):
        f = os.path.join(self.test_configs, 'estimate_choice_model.xml')
        config = XMLConfiguration(f).get_estimation_specification('choice_model_with_equations_template')
        should_be = {'_definition_': ['var1 = package.dataset.some_variable_or_expression'],
          -2: {1: ['constant'], 2: ['var1']}}
        self.assertEqual(config, should_be)

    def test_get_estimation_configuration_with_starting_values(self):
        f = os.path.join(self.test_configs, 'estimate_choice_model_w_starting_values.xml')
        model_name = 'model with starting_values'
        config = XMLConfiguration(f).get_estimation_configuration(model_name)
        config = config['config_changes_for_estimation'][model_name]
        should_be = {'estimate_config': {'starting_values': {'fixed_with_starting_value': (float(42.0), False),
                                         'non_fixed_with_starting_value': float(42.0),
                                         'guppy': float(12.5)}}}
        self.assertEqual(config, should_be)

    def test_expression_library(self):
        # Test that get_expression_library is functioning correctly; that computing variables defined in the library
        # give the correct answers; and that the expression library is set correctly  for estimation and run configurations.
        f = os.path.join(self.test_configs, 'expression_library_test.xml')
        config = XMLConfiguration(f)
        lib = config.get_expression_library()
        # NOTE: the 'income_less_than' parameterized variable is a future feature that has not been implemented yet
        # (so it can't be used yet in computing variables).
        lib_should_be = {('test_agent', 'income'): 'income',
                     ('test_agent', 'income_times_2'): 'opus_core.test_agent.income_times_2',
                     ('test_agent', 'i2'): 'opus_core.test_agent.income_times_2',
                     ('test_agent', 'income_times_10'): '5*opus_core.test_agent.income_times_2',
                     ('test_agent', 'income_times_10_ds_qualified'): '5*test_agent.income_times_2',
                     ('test_agent', 'income_times_10_using_primary'): '10*test_agent.income',
                     ('test_agent', 'income_times_20_using_lib'): '2*test_agent.income_times_10_using_primary',
                     ('test_agent', 'income_less_than'): 'def income_less_than(i): return test_agent.income<i',
                     ('parcel', 'ln_cost'): 'ln(psrc.parcel.cost)',
                     ('parcel', 'bsqft'): 'urbansim_parcel.parcel.building_sqft',
                     ('parcel', 'existing_units'): 'urbansim_parcel.parcel.existing_units'}
        self.assertEqual(lib, lib_should_be)

        # Test that computing the value of this variable gives the correct answer.  This involves
        # setting the expression library in VariableFactory -- when actually estimating a model or running
        # a simulation, that gets done by a call in ModelSystem.run.
        VariableFactory().set_expression_library(lib)
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='test_agents', table_data={"income":array([1,5,10]), "id":array([1,3,4])})
        dataset = Dataset(in_storage=storage, in_table_name='test_agents', id_name="id", dataset_name="test_agent")
        # test getting a primary attribute
        result1 = dataset.compute_variables(["test_agent.income"])
        self.assert_(ma.allclose(result1, array([1, 5, 10]), rtol=1e-6))
        # test with and without package name for a variable defined as a Python class
        result2 = dataset.compute_variables(["test_agent.income_times_2"])
        result3 = dataset.compute_variables(["test_agent.i2"])
        result4 = dataset.compute_variables(["opus_core.test_agent.income_times_2"])
        self.assert_(ma.allclose(result2, array([2, 10, 20]), rtol=1e-6))
        self.assert_(ma.allclose(result3, array([2, 10, 20]), rtol=1e-6))
        self.assert_(ma.allclose(result4, array([2, 10, 20]), rtol=1e-6))
        result5 = dataset.compute_variables(["test_agent.income_times_10"])
        result6 = dataset.compute_variables(["test_agent.income_times_10_ds_qualified"])
        result7 = dataset.compute_variables(["test_agent.income_times_10_using_primary"])
        result8 = dataset.compute_variables(["test_agent.income_times_20_using_lib"])
        self.assert_(ma.allclose(result5, array([10, 50, 100]), rtol=1e-6))
        self.assert_(ma.allclose(result6, array([10, 50, 100]), rtol=1e-6))
        self.assert_(ma.allclose(result7, array([10, 50, 100]), rtol=1e-6))
        self.assert_(ma.allclose(result8, array([20, 100, 200]), rtol=1e-6))
        # Test that the expression library is set correctly for estimation and run configurations.
        est = config.get_estimation_configuration()
        self.assertEqual(est['expression_library'], lib_should_be)
        run = config.get_run_configuration('test_scenario')
        self.assertEqual(run['expression_library'], lib_should_be)

        f = os.path.join(self.test_configs, 'expression_library_raises_test.xml')
        config = XMLConfiguration(f)
        self.assertRaises(SyntaxError, config.get_expression_library)

    def test_estimation_configuration(self):
        f = os.path.join(self.test_configs, 'nlm_config.xml')
        config = XMLConfiguration(f)
        estimation_config = config.get_estimation_configuration('nlm_model')
        # the nlm has some starting values given, we need to make sure that they end up in the
        # estimation_config overrides for the model
        changes_config = estimation_config['config_changes_for_estimation']['nlm_model']
        should_be = {'estimate_config': {'starting_values': {'default_name': float(42.0), 'explicit_name': float(0.42)}}}
        self.assertEqual(changes_config, should_be)

    def test_save_as(self):
        # test saving as a new file name - this should also test save()
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        c = XMLConfiguration(f)
        str_io = StringIO.StringIO()
        c.save_as(file_object = str_io)
        # compare the strings removing white space
        saved_root = fromstring(str_io.getvalue())
        # rather than typing it in here, just read the value from the file
        est_file = open(f)
        should_be_root = fromstring(est_file.read())
        self.assertElementsEqual(saved_root, should_be_root, include_tree = True)
        str_io.close()
        est_file.close()

    def test_update_and_initialize(self):
        # Try update with a completely different project - make sure stuff gets replaced.
        # Then reinitialize from the file and check that it reverts.
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        config = XMLConfiguration(f)
        update_str = """<?xml version='1.0' encoding='UTF-8'?>
            <opus_project>
              <scenario_manager>
                <scenario name="test_scenario" type="scenario">
                  <i type="integer">42</i>
                </scenario>
              </scenario_manager>
            </opus_project>"""
        config.update(update_str)
        section1 = config.get_section('scenario_manager/scenario', name = 'test_scenario')
        self.assertEqual(section1, {'i': 42})
        # no expression_library section in the updated configuration
        section2 = config.get_section('general/expression_library')
        self.assertEqual(section2, None)
        # now re-initialize from the original xml file, which has an expression_library section and no scenario manager section
        config.initialize_from_xml_file()
        section3 = config.get_section('scenario_manager/scenario', 'test_scenario')
        self.assertEqual(section3, None)
        section4 = config.get_section('general/expression_library')
        self.assertEqual(section4['ln_cost'], 'ln(psrc.parcel.cost)+100')

    def test_update_and_save(self):
        # make sure nodes marked as temporary or inherited are filtered out when doing an update and a save
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        config = XMLConfiguration(f)
        update_str = """
        <opus_project>
            <general>
              <parent type="file">child1.xml</parent>
              <parent type="file">child2.xml</parent>
              <expression_library type="dictionary" >
                <variable name="ln_cost" type="variable_definition" >ln(psrc.parcel.cost+100)</variable>
                <variable name="tax" type="variable_definition" inherited="child1">urbansim_parcel.parcel.tax</variable>
              </expression_library>
            </general>
            <data_manager inherited="someplace" />
            <results_manager temporary="True" />
            <model_manager>
              <estimation type="dictionary" >
                <real_estate_price_model type="dictionary" />
               </estimation>
            </model_manager>
           <scenario_manager/>
          </opus_project>
        """
        config.update(update_str)
        str_io = StringIO.StringIO()
        config.save_as(file_object = str_io)
        saved_root = fromstring(str_io.getvalue())
        should_be_root = fromstring(
        """
          <opus_project>
            <general>
              <parent type="file">child1.xml</parent>
              <parent type="file">child2.xml</parent>
              <expression_library type="dictionary">
                <variable name="ln_cost" type="variable_definition">ln(psrc.parcel.cost+100)</variable>
              </expression_library>
            </general>
            <model_manager>
              <estimation type="dictionary">
                <real_estate_price_model type="dictionary" />
              </estimation>
            </model_manager>
           <scenario_manager />
          </opus_project>
          """)
        self.assertElementsEqual(saved_root, should_be_root, include_tree = True)
        str_io.close()

    def test_followers(self):
        # Read in an xml configuration that includes a 'followers' attribute.
        # Make sure that the resulting configuration has the nodes in the correct order
        # Then write it out, and make sure the followers attribute is still correct.
        f = os.path.join(self.test_configs, 'followers_test_child.xml')
        config = XMLConfiguration(f)
        mydict = config.full_tree.find('general/mydict')
        child_names = map(lambda n: n.tag, mydict.iterchildren(tag=Element))
        self.assertEqual(child_names, ['a', 'b', 'x', 'c', 'd'])
        # Now update the configuration with a new xml tree, in which x is after c and
        # there is also a new node e
        update_str = """
          <opus_project>
            <general>
              <parent type="file">followers_test_parent.xml</parent>
              <mydict type="dictionary">
                <a type="string" inherited="followers_test_parent">atest</a>
                <b type="string" inherited="followers_test_parent">btest</b>
                <c type="string" inherited="followers_test_parent">ctest</c>
                <x type="string" followers="d">xtest</x>
                <d type="string" inherited="followers_test_parent">dtest</d>
                <e type="string">etest</e>
               </mydict>
            </general>
          </opus_project>"""
        config.update(update_str)
        # make sure the 'followers' attribute is updated correctly
        self.assertEqual(config.full_tree.find('general/mydict/x').get('followers'), 'd')
        # now write it out to a StringIO file-like object, and make sure it has
        # the correct contents
        str_io = StringIO.StringIO()
        config.save_as(file_object = str_io)
        element_saved = fromstring(str_io.getvalue())
        # squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        element_should_be = fromstring("""
          <opus_project>
            <general>
              <parent type="file">followers_test_parent.xml</parent>
              <mydict type="dictionary">
                <x followers="d" type="string">xtest</x>
                <e type="string">etest</e>
               </mydict>
            </general>
          </opus_project>""")
        # squished_should_be = should_be.replace(' ', '').replace('\n', '')
        self.assertElementsEqual(element_saved, element_should_be, include_tree = True)
        str_io.close()

    def test_error_handling(self):
        # there isn't an xml configuration named badname.xml
        self.assertRaises(IOError, XMLConfiguration, 'badname.xml')
        # badconfig1 has a syntax error in the xml
        f1 = os.path.join(self.test_configs, 'badconfig1.xml')
        self.assertRaises(SyntaxError, XMLConfiguration, f1)
        # badconfig2 doesn't have a root element called project
        f2 = os.path.join(self.test_configs, 'badconfig2.xml')
        self.assertRaises(ValueError, XMLConfiguration, f2)
        # badconfig3 is well-formed, but doesn't have a scenario_manager section
        # (so getting the run configuration from it doesn't work)
        f3 = os.path.join(self.test_configs, 'badconfig3.xml')
        config3 = XMLConfiguration(f3)
        self.assertRaises(ValueError, config3.get_run_configuration, 'test_scenario')
        # badconfig4 is well-formed, with a scenario_manager section,
        # but there isn't a scenario named test_scenario
        f4 = os.path.join(self.test_configs, 'badconfig4.xml')
        config4 = XMLConfiguration(f4)
        self.assertRaises(ValueError, config4.get_run_configuration, 'test_scenario')
        # badconfig5 has an empty string for an integer value, but no parser directive to turn it to None
        f5 = os.path.join(self.test_configs, 'badconfig5.xml')
        config5 = XMLConfiguration(f5)
        self.assertRaises(ValueError, config5.get_run_configuration, 'test_scenario')
        # badconfig_xml_version_too_small has an xml version number less than the minumum
        f_small = os.path.join(self.test_configs, 'badconfig_xml_version_too_small.xml')
        self.assertRaises(XMLVersionException, XMLConfiguration, f_small)
        # badconfig_xml_version_too_big has an xml version number greater than the maximum
        f_big = os.path.join(self.test_configs, 'badconfig_xml_version_too_big.xml')
        self.assertRaises(XMLVersionException, XMLConfiguration, f_big)

    # we don't really support old configurations
    def skip_test_convert_model_to_dict(self):
        # new structure with type='model'
        f_new = os.path.join(self.test_configs, 'new_model_struct.xml')
        # old structure with type='dictionary'
        f_old = os.path.join(self.test_configs, 'old_model_struct.xml')
        # should translate to exactly the same dict
        new_conf = XMLConfiguration(f_new).get_section('model_manager/models/model', 'regmodel')
        old_conf = XMLConfiguration(f_old).get_section('model_manager/models/model', 'regmodel')
        self.assertDictsEqual(old_conf, new_conf)

    def test_node_identity_string(self):
        node = XMLConfiguration(os.path.join(self.test_configs, 'node_ids.xml')).full_tree.getroot()
        par = node.find('node')
        sib1 = node.find('node/node')
        same1, same2, different1 = sib1.findall('node')
        different2 = sib1.find('child')
        same_path_as_sib1_but_longer = node.find('opus_project/node/node')
        f = node_identity_string # alias the long function name

        # full path is opus_project/opus_project/node/node
        # -- but the first opus_project is not included in id string
        same_path_expected = '/opus_project:/node:parent/node:sib1'
        self.assertEqual(f(same_path_as_sib1_but_longer), same_path_expected)
        same1_expected = '/node:parent/node:sib1/node:child'
        self.assertEqual(f(same1), same1_expected)
        self.assertEqual(f(same1), f(same2)) # two nodes that do have the same id
        self.assertNotEqual(f(same1), f(different1)) # diff name
        self.assertNotEqual(f(same1), f(different2)) # diff tag
        self.assertNotEqual(f(sib1), f(same_path_as_sib1_but_longer))

    def test_element_id(self):
        node1 = Element('node1')
        node2 = Element('node2', {'name': 'node2'})
        node3 = Element('node3', {'name': 'a node with a long name with spaces'})

        self.assertEqual(element_id(node1), '/node1:')
        self.assertEqual(element_id(node2), '/node2:node2')
        self.assertEqual(element_id(node3), '/node3:a node with a long name with spaces')

    def test_model_dependencies(self):
        f = os.path.join(self.test_configs, 'models.xml')
        xml = XMLConfiguration(f)
        regmdep = xml.model_dependencies("regmodel")
        should_be = {'variable': ['parcel.land_use_id', 'parcel.land_use_id>0', 'parcel.land_value'], 
                     'dataset': ['parcel']}
        self.assertDictsEqual(regmdep, should_be)
        depall = xml.model_dependencies()
        should_be = {'variable': ['parcel.land_use_id', 'parcel.land_use_id>0', 'parcel.land_value', 'building.residential_units'], 
                     'dataset': ['parcel', 'building', 'household']}
        self.assertDictsEqual(depall, should_be)
        
    def test_get_parent_no_parent(self):
        f = os.path.join(self.test_configs, 'parent1.xml')
        config = XMLConfiguration(f)
        self.assert_(config.get_first_writable_parent_file() is None, 'No parent')
        
    def test_get_parent_one_parent(self):
        f = os.path.join(self.test_configs, 'child2.xml')
        config = XMLConfiguration(f)
        self.assert_(re.match(r'.*parent1\.xml$', config.get_first_writable_parent_file()), 'One parent')
        
    def test_get_parent_two_parents(self):
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        config = XMLConfiguration(f)
        self.assert_(re.match(r'.*child1\.xml$', config.get_first_writable_parent_file()), 'First parent')

    def test_get_parent_two_parents_first_not_writable(self):
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        
        # Use a simple mockup: Simulate no write access for child1.xml
        try:
            old_os_access = os.access
            os.access = lambda f, m: False if m == os.W_OK and re.match(r'.*child1\.xml$', f) else old_os_access(f, m)
            config = XMLConfiguration(f)
            self.assert_(re.match(r'.*child2\.xml$', config.get_first_writable_parent_file()), 'Second parent')
        finally:
            os.access = old_os_access

if __name__ == '__main__':
    opus_unittest.main()

