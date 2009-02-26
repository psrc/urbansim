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

import copy, os, pprint
from numpy import array
from xml.etree.cElementTree import ElementTree, tostring
from opus_core.configuration import Configuration
from opus_core.configurations.xml_version import XMLVersion
from opus_core.version_numbers import minimum_xml_version, maximum_xml_version
from opus_core.opus_exceptions.xml_version_exception import XMLVersionException
from opus_core.variables.variable_name import VariableName


class XMLConfiguration(object):
    """
    An XMLConfiguration is a kind of configuration that represents a project
    and that can be stored or loaded from an XML file.
    """

    def __init__(self, filename, default_directory=None, is_parent=False):
        """Initialize this configuration from the contents of the xml file named by 'filename'.
        Look first in the default directory if present; otherwise in the directory in which
        the Opus code is stored.  If is_parent is true, mark all of the nodes as inherited
        (either from this configuration or a grandparent)."""
        self.full_filename = None
        if default_directory is not None:
            f = os.path.join(default_directory, filename)
            if os.path.exists(f):
                self.full_filename = f
        if self.full_filename is None:
            opus_core_dir = __import__('opus_core').__path__[0]
            workspace_dir = os.path.split(opus_core_dir)[0]
            self.full_filename = os.path.join(workspace_dir, filename)
        # if self.full_filename doesn't exist, ElementTree will raise an IOError
        # self.tree is the xml tree (without any inherited nodes);
        # self.full_tree is the xml tree with all the inherited nodes as well
        # parent_map is a dictionary that can be used to work back up the XML tree
        # these are all set by the _initialize method
        self.tree = None
        self.full_tree = None
        self.parent_map = None
        self.name = os.path.basename(self.full_filename).split('.')[0]
        self.pp = pprint.PrettyPrinter(indent=4)
        self.xml_version = XMLVersion()
        self.version_warning_message = ''
        self.initialize_from_xml_file(is_parent)

    def initialize_from_xml_file(self, is_parent=False):
        """initialize (or re-initialize) the contents of this configuration from the xml file.
        If is_parent is true, mark all of the nodes as inherited
        (either from this configuration or a grandparent)."""
        # try to load the element tree
        self._initialize(ElementTree(file=self.full_filename), is_parent)

    def update(self, newconfig_str):
        """Update the contents of this configuration from the string newconfig_str
        (a string representing an xml configuration).  Ignore any temporary or
        inherited nodes in newconfig_str (this gets freshly initialized)."""
        # Note that this doesn't change the name of this configuration, or the full_filename
        str_io = StringIO.StringIO(newconfig_str)
        etree = ElementTree(file=str_io)
        # remove any old followers nodes
        for n in self.full_tree.getiterator():
            if n.get('followers') is not None:
                # unfortunately it doesn't look like ElementTree has a method for removing an attribute ....
                del n.attrib['followers']
        self._set_followers(etree.getroot(), self._get_parent_trees(), '')
        self._clean_tree(etree.getroot())
        self._initialize(etree, False)

    def get_section(self, name):
        """Extract the section named 'name' from this xml project, convert it to a dictionary,
        and return the dictionary.  Return None if there isn't such a section.  If there are
        multiple sections with the given name, return the first one."""
        x = self._find_node(name)
        if x is None:
            return None
        else:
            return Configuration(self._node_to_config(x))

    def get_expression_library(self):
        """Return a dictionary of variables defined in the expression library for this configuration.  The keys in the
        dictionary are pairs (dataset_name, variable_name) and the values are the corresponding expressions."""
        result = {}
        node = self._find_node('general/expression_library')
        if node is not None:
            for v in node:
                # Add the variable to the dictionary, indexed by the pair (dataset,name)
                name = v.tag
                dataset = v.get('dataset')
                result[(dataset,name)] = v.text
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
        config = self.get_section('scenario_manager/%s' % name)
        if config is None:
            raise ValueError, "didn't find a scenario named %s" % name
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

        config_section = self.get_section('model_manager/model_system')
        config = config_section['estimation_config']
        self._merge_controllers(config)
        self._insert_expression_library(config)

        # we only need to check model specific overrides if the model is specified
        if model_name is None:
            return config

        config['model_name'] = model_name

        model_specific_overrides = {}

        # look if the configuration specifies a list of models to run before the given model when 
        # estimating it.
        mtr_path = ('model_manager/model_system/%s/structure/prepare_for_estimate/models_to_run/' 
                    % model_name)
        mtr_node = self._find_node(mtr_path)
        mtr_list = self._convert_node_to_data(mtr_node) if mtr_node is not None else []

        # if config_changes_for_estimation is given, the model system only sees that list of models
        # so we need to manually append the given model
        if model_group is None:
            mtr_list.append({model_name: ["estimate"]}) # append regular model
        else:
            group_members = {'group_members': [{model_group:['estimate']}]}
            mtr_list.append({model_name: group_members})

        if mtr_list is not None:
            model_specific_overrides['models'] = mtr_list

        # NOTE -- This is the place to add support for additional model specific
        # configuration like datasets_to_preload etc.
        
        # The model system doesn't like it when it gets an empty config_changes_for_estimation
        if len(model_specific_overrides) > 0:
            config['config_changes_for_estimation'] = {model_name: model_specific_overrides}
        return config

    def get_estimation_specification(self, model_name, model_group=None):
        """Get the estimation specification for the given model and return it as a dictionary."""
        # all_vars is the list of variables from the expression library
        all_vars = []
        lib_node = self._find_node('general/expression_library')
        for v in lib_node:
            # If the variable is defined as an expression, make an alias.
            # Otherwise it's a Python class.  If the name in the expression library
            # is the same as the variable short name, just use it as is; otherwise
            # also set up an alias.
            if v.get('source')=='expression':
                add_alias = True
            else:
                n = VariableName(v.text)
                add_alias = n.get_short_name()!=v.tag
            if add_alias:
                all_vars.append('%s = %s' % (v.tag, v.text))
            else:
                all_vars.append(v.text)
        # sort the list of variables to make it easier to test the results
        all_vars.sort()
        # fetch list of submodels
        submodel_list = self.get_section('model_manager/model_system/%s/specification/' % model_name)
        result = {}
        result['_definition_'] = all_vars
        if model_group is not None:
            model_dict = submodel_list[model_group]
            result_group = {model_group:result}
        else:
            model_dict = submodel_list
        if model_dict and isinstance(model_dict, dict):
            for submodel_name in model_dict.keys():
                submodel = model_dict[submodel_name]
                if 'variables' in submodel.keys():
                    result[submodel['submodel_id']] = submodel['variables']
                else: # specification has equations
                    result[submodel['submodel_id']] = {}
                    for equation_name in submodel.keys():
                        if equation_name!='description' and equation_name!='submodel_id':
                            equation_spec = submodel[equation_name]
                            result[submodel['submodel_id']][equation_spec['equation_id']] = equation_spec['variables']
        if model_group is not None:
            result = result_group
        return result

    def save(self):
        """save this configuration in a file with the same name as the original"""
        self.save_as(self.full_filename)

    def save_as(self, name):
        """save this configuration under a new name"""
        # TODO: change name???
        self._indent(self.tree.getroot())
        self.tree.write(name)

    def find(self, path):
        """return the string encoding of the node referenced by 'path', or None if there is no such node"""
        n = self._find_node(path)
        if n is None:
            return n
        else:
            return tostring(n)

    def get_opus_data_path(self):
        """return the path to the opus_data directory.  This is found in the environment variable
        OPUS_DATA_PATH, or if that environment variable doesn't exist, as the contents of the
        environment variable OPUS_HOME followed by 'data' """
        path = os.environ.get('OPUS_DATA_PATH')
        if path is None:
            return os.path.join(os.environ.get('OPUS_HOME'), 'data')
        else:
            return path

    def _initialize(self, elementtree, is_parent):
        self.tree = elementtree
        self.full_tree = copy.deepcopy(self.tree)
        full_root = self.full_tree.getroot()
        if full_root.tag!='opus_project':
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
        for p in self._get_parent_trees():
            self._merge_parent_elements(p, '')
        if is_parent:
            for n in full_root.getiterator():
                if n.get('inherited') is None:
                    n.set('inherited', self.name)
        # Parent map... can be used for working back up the XML tree
        self.parent_map = dict((c, p) for p in self.full_tree.getiterator() for c in p)

    def _find_node(self, path):
        # find path in my xml tree
        # this is like the 'find' provided by ElementTree, except that it also works with an empty path
        # Caution: in ElementTree an element without any elements tests as False -- so if you are using
        # the result of _find_node in an 'if' statement, check that the result is not None explicitly.
        if path=='':
            return self.full_tree.getroot()
        else:
            return self.full_tree.getroot().find(path)

    def _get_parent_trees(self):
        default_dir = os.path.split(self.full_filename)[0]
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


    def _merge_parent_elements(self, parent_node, path):
        # parent_node is a node someplace in a parent tree, and path is a path from the root
        # to that node.  Merge in parent_node into this configuration's tree.  We are allowed
        # to reuse bits of the xml from parent_node.  (The xml for it is created by this class
        # from its file during initialization, so we don't need to make a copy).
        # Precondition: path gives a unique element in this configuration's xml tree.
        # First merge in any attributes from the parent that aren't in the child (except for 'inherited' attributes)
        this_node = self._find_node(path)
        for k in parent_node.keys():
            if k!='inherited' and k not in this_node.attrib:
                this_node.set(k, parent_node.get(k))
        prev_child = None
        for child in parent_node.getchildren():
            if path=='':
                extended_path = child.tag
            else:
                extended_path = path + '/' + child.tag
            if self._find_node(extended_path) is None:
                # 'child' doesn't exist in this tree, so we can just add it and all its children.
                # We want to insert it at a sensible place in the tree.  If there are any nodes
                # already in the tree with a 'followers' attribute that includes the name of the
                # new node being inserted, we need to put the new node after those nodes.
                # Also, in the parent, 'child' is right after 'prev_child', and so in the new tree we put
                # 'child' right after the local version of 'prev_child', unless one of the tags in a
                # 'followers' attribute says it has to go later.  If 'prev_child' is not None, we know that
                # this tree will have a node with the same tag as 'prev_child' node, because
                # either it was already in this tree, or we just merged it in from the parent.
                # (One thing that may be odd about this is if there are several nodes with the
                # same tag as prev_child -- in this case we'll use the last one.)
                where = 0
                i = 0
                for c in self._find_node(path).getchildren():
                    f = c.get('followers')
                    if (f is not None and child.tag in f.split(',')) or (prev_child is not None and c.tag==prev_child.tag):
                        where = i+1
                    i = i+1
                self._find_node(path).insert(where,child)
            else:
                # 'child' does exist in this tree.  Keep going further with
                # its children, in case some of them don't exist in this tree
                self._merge_parent_elements(child, extended_path)
            prev_child = child

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
            if level and (not element.tail or not element.tail.strip()):
                element.tail = i

    def _set_followers(self, tree, parent_trees, path):
        # Recursively traverse tree, setting the 'followers' attribute on any node
        # that needs it.  A node n should have a 'followers' attribute if it is new in
        # 'tree' and doesn't occur in any parent.  If so, 'followers' should be a
        # comma-separated list of names of inherited nodes that follow n.  (This is used
        # when merging in inherited nodes to put them in the right place.)
        children = tree.getchildren()
        i = 0
        while i<len(children):
            n = children[i]
            if n.get('inherited') is None:
                is_new = True
                if path=='':
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
            i = i+1

    def _merge_controllers(self, config):
        '''merge the controllers in model_manager/model_system/ portion if the
        project (if any) into config.'''

        my_controller_configuration = self.get_section('model_manager/model_system')

        if my_controller_configuration is not None:
            if "models_configuration" not in config:
                config["models_configuration"] = {}
            for model in my_controller_configuration.keys():
                if model not in config["models_configuration"].keys():
                    config["models_configuration"][model] = {}
                config['models_configuration'][model]['controller'] = my_controller_configuration[model]

    def _node_to_config(self, node):
        config = {}
        for child in node:
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
            for child in included:
                self._add_to_dict(child, result_dict)
        elif action in ['only_for_includes', 'skip']:
            pass
        else:
            data = self._convert_node_to_data(node)
            type_name = node.get('type')
            if type_name=='category' or type_name=='category_with_special_keys':
                result_dict.update(data)
            elif 'config_name' in node.attrib:
                result_dict[node.get('config_name')] = data
            elif type_name == 'model_template':
                pass # we dont want templates in dicts
            else:
                result_dict[node.tag] = data

    def _convert_node_to_data(self, node):
        # convert the information under node into the appropriate Python datatype.
        # To do this, branch on the node's type attribute.  For some kinds of data,
        # return None if the node should be skipped.
        # For example, for type="model_choice" return None if that is a model
        # that isn't selected to be run
        type_name = node.get('type')
        if type_name=='integer':
            return self._convert_string_to_data(node, int)
        elif type_name=='float':
            return self._convert_string_to_data(node, float)
        elif type_name=='string' or type_name=='password' or \
             type_name=='variable_definition' or type_name=='path':
            return self._convert_string_to_data(node, str)
        elif type_name=='quoted_string':
            if node.text is not None:
                return "'%s'" % node.text
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
        elif type_name in ['dictionary', 'category', 'submodel',
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
        elif type_name=='model_choice':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='table':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='dataset':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='variable':
            return self._convert_custom_type_to_data(node, "Skip")
        elif type_name=='python_code':
            return eval(node.text)
        else:
            raise ValueError, 'unknown type: %s' % type_name

    def _make_instance(self, class_name, path, keyword_args={}):
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
        blank_to_None = node.get('parser_action', '')=='blank_to_None'
        if node.text is None:
            if blank_to_None:
                return None
            elif func==str:
                return ''
            else:
                raise ValueError, "found empty string in xml node but no parser action to convert it to None"
        else:
            if blank_to_None and node.text == 'None':
                return None
            return func(node.text)

    def _convert_list_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node)
        result_list = filter(lambda n: n is not None, r)
        if node.get('parser_action', '')=='list_to_dictionary':
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

    def _convert_variable_list_to_data(self, node):
        # node should be a text node with a comma-separated list of variable
        # names (perhaps with white space as well)
        if node.text is None:
            return [] # this is the case with xml stumps (like: <var_list />)
        else:
            return map(lambda s: s.strip(), node.text.split(','))

    def _convert_tuple_to_data(self, node):
        r = map(lambda n: self._convert_node_to_data(n), node)
        return tuple(r)

    def _convert_file_or_directory_to_data(self, node):
        if node.get('parser_action', '')=='prefix_with_opus_data_path':
            return os.path.join(self.get_opus_data_path(), node.text)
        else:
            return node.text

    def _convert_dictionary_to_data(self, node):
        result_dict = {}
        for child in node:
            self._add_to_dict(child, result_dict)
        return result_dict

    def _convert_model_to_dict(self, node):
        '''translate from xml structure to dictionary configuration.'''
        structure_node = node.find('structure')
        if structure_node == None: # invalid format of model node
            raise StandardError('XML Error: Invalid Model structure: '
                  'Model %s is missing a "structure" tag' %node.tag)
        model_dict = {}
        for subnode in structure_node:
            # append 'arguments' to some nodes
            if subnode.tag in ['init', 'run', 'prepare_for_run',
                               'estimate', 'prepare_for_estimate']:
                subnode_struct = {'arguments':{}}
                # everything but 'name' and 'output' should be under arguments
                for arg_node in subnode:
                    if not arg_node.tag in ['name', 'output']:
                        self._add_to_dict(arg_node, subnode_struct['arguments'])
                    else:
                        self._add_to_dict(arg_node, subnode_struct)
                model_dict[subnode.tag] = subnode_struct
            elif subnode.tag == 'import':
                # dicts wants module (with path) as key and class name as value
                try:
                    model_module = subnode.find("module").text
                    model_classname = subnode.find("classname").text
                    model_dict['import'] = {model_module: model_classname}
                except AttributeError:
                    print('Error: Import tag should have two child nodes;'
                          'module and classpath. Model "%s" will not work '
                          'correctly.' %node.tag)
                    model_dict['import'] = None
            else: # just put it in the dict
                model_dict[subnode.tag] = self._convert_node_to_data(subnode)
        return model_dict

    def _convert_dictionary_with_special_keys_to_data(self, node):
        # Node should be converted to a dictionary of dictionaries, typically with keys in the top-level dictionary
        # that are integers.  Since in xml tags can't be integers, this is handled with this special type.  The
        # elements under the node are parsed into dictionaries (their tags don't matter).  The node must have an
        # attribute 'key_name'.  The key name is used to find the key for each element in the top-level dictionary,
        # and is deleted from the second-level dictionary.
        # See the unit tests for an example - that may make it clearer what this does.
        key_name = node.get('key_name')
        result = {}
        for child in node:
            d = self._convert_node_to_data(child)
            k = d[key_name]
            del d[key_name]
            result[k] = d
        return result

    def _convert_class_to_data(self, node):
        items = {}
        for child in node:
            self._add_to_dict(child, items)
        class_name = items['Class_name']
        class_path = items['Class_path']
        # Special case database configs as they may contain a database_connection which
        # references another part of the XML.  We need to add those elements to the
        # dictionary if they are defined in that config before calling _make_instance
        if class_name == 'DatabaseConfiguration':
            # Look for a database_connection element...
            if items.has_key('database_connection'):
                database_hook = items['database_connection']
                #print "Found a database_hook = %s" % (database_hook)
                # Next, since we have a connection we must go find it in the data manager
                the_database = self.get_section('general/database_library/%s' %
                                                (database_hook))
                if the_database:
                    #print "Converting a database connection into a class"
                    #self.pp.pprint(the_database)
                    items.update(the_database)
                    #self.pp.pprint(items)
                # Get rid of the database_connection element since we just replaced it
                # with the real connection info
                del items['database_connection']
        # delete the class name and class path from the dictionary -- the remaining items
        # will be the keyword arguments to use to create the instance
        del items['Class_name']
        del items['Class_path']
        i = self._make_instance(class_name, class_path, items)
        if node.get('parser_action', '')=='execute':
            return i.execute()
        else:
            return i

    def _convert_custom_type_to_data(self, node, skip):
        # skip is a string that is the value when this node should be skipped
        if node.text==skip:
            return None
        name = node.tag
        children = node.getchildren()
        if len(children)==0:
            return name
        else:
            subdict = {}
            for child in children:
                self._add_to_dict(child, subdict)
            return {name: subdict}

    def _insert_expression_library(self, config):
        # insert the expression library into config, if it isn't empty
        lib = self.get_expression_library()
        if len(lib)>0:
            config['expression_library'] = lib

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

    def test_types(self):
        f = os.path.join(self.test_configs, 'manytypes.xml')
        config = XMLConfiguration(f).get_section('test_section')
        self.assertEqual(config,
                         {'description': 'a test configuration',
                          'quotedthing': r"'test\test'",
                          'empty1': '',
                          'empty2': None,
                          'emptypassword': None,
                          'year': 1980,
                          'mybool': True,
                          'ten': 10.0,
                          'emptyint': None,
                          'emptyfloat': None,
                          'years': (1980, 1981),
                          'list_test': [10, 20, 30],
                          'vars': ['population', 'employment', 'density'],
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
        # the ln_cost variable is redefined in child1, so it shouldn't have the 'inherited' attribute
        ln_cost_node = expression_library_node.find('ln_cost')
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is new, so also shouldn't have the 'inherited' attribute
        tax_node = expression_library_node.find('tax')
        self.assertEqual(tax_node.get('inherited'), None)
        # the existing_units variable is inherited and not overridden, so it should have 'inherited' set to the name of the parent
        existing_units_node = expression_library_node.find('existing_units')
        self.assertEqual(existing_units_node.get('inherited'), 'parent1')

    def test_grandchild_inherited_nodes(self):
        # test two levels of inheritance, with multiple inheritance as well
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        expression_library_node = XMLConfiguration(f).full_tree.find('general/expression_library')
        # the ln_cost variable is redefined in grandchild, so it shouldn't have the 'inherited' attribute
        ln_cost_node = expression_library_node.find('ln_cost')
        self.assertEqual(ln_cost_node.get('inherited'), None)
        # the tax variable is inherited from child1 (there is also a definition in child2 but that
        # shouldn't be used)
        tax_node = expression_library_node.find('tax')
        self.assertEqual(tax_node.get('inherited'), 'child1')
        # the extratax variable is inherited from child2
        extratax_node = expression_library_node.find('extratax')
        self.assertEqual(extratax_node.get('inherited'), 'child2')
        # the existing_units variable is inherited from parent1
        existing_units_node = expression_library_node.find('existing_units')
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

    def test_find(self):
        # test the 'find' method on inherited and non-inherited nodes
        f = os.path.join(self.test_configs, 'child1.xml')
        config = XMLConfiguration(f)
        ln_cost_str = config.find('general/expression_library/ln_cost')
        should_be = '<ln_cost dataset="parcel" source="expression" type="variable_definition" use="model variable">ln(psrc.parcel.cost)+10</ln_cost>'
        self.assertEqual(ln_cost_str.strip(), should_be)
        existing_units_str = config.find('general/expression_library/existing_units')
        expected = '<existing_units dataset="parcel" inherited="parent1" source="Python class" type="variable_definition" use="model variable">urbansim_parcel.parcel.existing_units</existing_units>'
        self.assertEqual(existing_units_str.strip(), expected)
        squid_str = config.find('model_manager/estimation/squid')
        self.assertEqual(squid_str, None)

    def test_get_controller(self):
        # test getting a run specification that includes a controller in the xml
        f = os.path.join(self.test_configs, 'controller_test.xml')
        config = XMLConfiguration(f).get_run_configuration('baseline')
        should_be = {'project_name':'test_project',
                    'models_configuration': {'real_estate_price_model': {'controller': {'prepare_for_run': {
          'name': 'prepare_for_run',
          'arguments': {'specification_storage': 'base_cache_storage', 'specification_table': 'real_estate_price_model_specification'}
          }}}}}
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
          24: ['ln_cost', 'existing_units', 'bsqft']}
        self.assertEqual(config, should_be)

    def test_get_estimation_specification_with_equation(self):
        f = os.path.join(self.test_configs, 'estimate_choice_model.xml')
        config = XMLConfiguration(f).get_estimation_specification('choice_model_with_equations_template')
        should_be = {'_definition_': ['var1 = package.dataset.some_variable_or_expression'],
          -2: {1: ['constant'], 2: ['var1']}}
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
        self.assert_(ma.allclose(result5, array([10, 50, 100]), rtol=1e-6))
        self.assert_(ma.allclose(result6, array([10, 50, 100]), rtol=1e-6))
        self.assert_(ma.allclose(result7, array([10, 50, 100]), rtol=1e-6))
        # Test that the expression library is set correctly for estimation and run configurations.
        est = config.get_estimation_configuration()
        self.assertEqual(est['expression_library'], lib_should_be)
        run = config.get_run_configuration('test_scenario')
        self.assertEqual(run['expression_library'], lib_should_be)

    def test_save_as(self):
        # test saving as a new file name - this should also test save()
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        c = XMLConfiguration(f)
        str_io = StringIO.StringIO()
        c.save_as(str_io)
        # compare the strings removing white space
        squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        # rather than typing it in here, just read the value from the file
        est_file = open(f)
        should_be = est_file.read().replace(' ', '').replace('\n', '')
        self.assertEqual(squished_result, should_be)
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
                <test_scenario type="scenario">
                  <i type="integer">42</i>
                  </test_scenario>
              </scenario_manager>
            </opus_project>"""
        config.update(update_str)
        section1 = config.get_section('scenario_manager/test_scenario')
        self.assertEqual(section1, {'i': 42})
        # no expression_library section in the updated configuration
        section2 = config.get_section('general/expression_library')
        self.assertEqual(section2, None)
        # now re-initialize from the original xml file, which has an expression_library section and no scenario manager section
        config.initialize_from_xml_file()
        section3 = config.get_section('scenario_manager/test_scenario')
        self.assertEqual(section3, None)
        section4 = config.get_section('general/expression_library')
        self.assertEqual(section4['ln_cost'], 'ln(psrc.parcel.cost)+100')

    def test_update_and_save(self):
        # make sure nodes marked as temporary or inherited are filtered out when doing an update and a save
        f = os.path.join(self.test_configs, 'grandchild1.xml')
        config = XMLConfiguration(f)
        update_str = """<opus_project>
            <general>
              <parent type="file">child1.xml</parent>
              <parent type="file">child2.xml</parent>
              <expression_library type="dictionary" >
                <ln_cost type="variable_definition" >ln(psrc.parcel.cost+100)</ln_cost>
                <tax type="variable_definition" inherited="child1">urbansim_parcel.parcel.tax</tax>
              </expression_library>
            </general>
            <data_manager inherited="someplace">
            </data_manager>
            <results_manager temporary="True">
            </results_manager>
            <model_manager>
              <estimation type="dictionary" >
                <real_estate_price_model type="dictionary" >
                </real_estate_price_model>
               </estimation>
            </model_manager>
           <scenario_manager/>
          </opus_project>"""
        config.update(update_str)
        str_io = StringIO.StringIO()
        config.save_as(str_io)
        # compare the strings removing white space
        squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        should_be = """
          <opus_project>
            <general>
              <parent type="file">child1.xml</parent>
              <parent type="file">child2.xml</parent>
              <expression_library type="dictionary">
                <ln_cost type="variable_definition">ln(psrc.parcel.cost+100)</ln_cost>
               </expression_library>
            </general>
            <model_manager>
              <estimation type="dictionary">
                <real_estate_price_model type="dictionary">
                </real_estate_price_model>
               </estimation>
            </model_manager>
           <scenario_manager />
          </opus_project>"""
        squished_should_be = should_be.replace(' ', '').replace('\n', '')
        self.assertEqual(squished_result, squished_should_be)
        str_io.close()

    def test_followers(self):
        # Read in an xml configuration that includes a 'followers' attribute.
        # Make sure that the resulting configuration has the nodes in the correct order
        # Then write it out, and make sure the followers attribute is still correct.
        f = os.path.join(self.test_configs, 'followers_test_child.xml')
        config = XMLConfiguration(f)
        mydict = config.full_tree.find('general/mydict')
        child_names = map(lambda n: n.tag, mydict.getchildren())
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
                <x type="string" followers="c,d">xtest</x>
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
        config.save_as(str_io)
        squished_result = str_io.getvalue().replace(' ', '').replace('\n', '')
        should_be = """
          <opus_project>
            <general>
              <parent type="file">followers_test_parent.xml</parent>
              <mydict type="dictionary">
                <x followers="d" type="string">xtest</x>
                <e type="string">etest</e>
               </mydict>
            </general>
          </opus_project>"""
        squished_should_be = should_be.replace(' ', '').replace('\n', '')
        self.assertEqual(squished_result, squished_should_be)
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

    def test_convert_model_to_dict(self):
        # new structure with type='model'
        f_new = os.path.join(self.test_configs, 'new_model_struct.xml')
        # old structure with type='dictionary'
        f_old = os.path.join(self.test_configs, 'old_model_struct.xml')
        # should translate to exactly the same dict
        new_conf = XMLConfiguration(f_new).get_section('model_manager/model_system')['regmodel']
        old_conf = XMLConfiguration(f_old).get_section('model_manager/model_system')['regmodel']
        self.assertDictsEqual(old_conf, new_conf)


if __name__ == '__main__':
    opus_unittest.main()

