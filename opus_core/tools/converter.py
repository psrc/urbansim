# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml import etree
from xml.etree import cElementTree # read with cElementTree to strip comments
import copy

class Converter(object):

    '''
    Utility class to convert XML files from 1.0 to 2.0 format.

    The conversion is done in two steps; Check and Execute.
    The first step, checking, collects a list of actions to perform in self.actions_, and the list
    can be inspected before going on to the second step which executes the actions on the loaded XML
    file.

    This module can be invoked as a command line utility.
    '''

    def __init__(self, quiet = False, verbose = False):
        self.root = None
        self.actions_ = []
        self.warnings = []
        self.successfuls = []
        self.quiet = quiet
        self.verbose = verbose

    def _path_to_node(self, node):
        if node is self.root:
            return ''
        parent_path = self._path_to_node(node.getparent())
        if not parent_path:
            return node.tag
        return '%s/%s' % (parent_path, node.tag)

    def xml_string(self):
        node = copy.deepcopy(self.root)
        self._indent(node)
        return etree.tostring(node)

    def write(self, text):
        if not self.quiet:
            print text

    def verbose_write(self, text):
        if self.verbose and not self.quiet:
            print text

    def execute(self):
        self.counter_successful = 0
        self.warnings = []
        action_categories = {}
        action_counter = 0
        for action_docstring, action_function, action_object in self.actions_:
            if action_docstring not in action_categories:
                action_categories[action_docstring] = [action_object,]
            else:
                action_categories[action_docstring].append(action_object)
            action_counter = action_counter + 1
            try:
                action_function()
                self.successfuls.append('%s: %s' % (action_docstring, action_object))
                self.verbose_write('[OK] %s: %s' % (action_docstring, action_object))
            except Exception, ex:
                self.warnings.append('%s: %s' % (ex, action_object))
                self.verbose_write('[Warning] %s: %s\n    %s' % (action_docstring, action_object, ex))
        # print summary
        for category in action_categories:
            self.write('Executed %s %d time(s)' %(category, len(action_categories[category])))
        count = 0
        for warning in self.warnings:
            count = count + 1
            self.write('Warning [%d]: %s' % (count, warning))
        self.write('Total of %d actions. %d OK, %d skipped' %
                   (action_counter, len(self.successfuls), len(self.warnings)))

    def node_path(self, node, head_node = True):
        if node.getparent() is None:
            return ''
        if head_node:
            return '%s' % self.node_path(node.getparent(), head_node = False)
        return '%s/%s' % (self.node_path(node.getparent(), head_node = False), node.tag)

    def add_action(self, action, node, *additional_args):
        # operation object is the string that describes what the action operates on
        # it is used for logging purposes
        operation_object = '[No object]'
        if node is None and len(additional_args) > 0:
            operation_object = str(additional_args[0])
        elif node is not None:
            operation_object = self.node_path(node)
        # curry the function call
        def action_function(func = action, node = node, additional_args = additional_args):
            if not additional_args:
                func(node)
            elif node is None and additional_args:
                func(*additional_args)
            else: # node and additional arguments
                func(node, *additional_args)
        self.actions_.append((action.__doc__, action_function, operation_object))

    def tag_name_fix(self, node, should_be_tag):
        if node.tag != should_be_tag or node.get('name') is None:
            self.add_action(self.action_tag_to_name, node, should_be_tag)

    def _indent(self, element, level=0):
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

    def action_change_node_attrib(self, node, attr_dict):
        '''Change node attributes'''
        # deletes the attribute if the value for an attribute is None
        for key, value in attr_dict.items():
            if value is None:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, value)

    def action_update_version(self, node):
        '''Update the XML version string to 2.0'''
        print 'update version'
        if node is None:
            # create new version Element
            print 'adding xml_version'
            node = etree.Element('xml_version')
            node.text = '2.0'
            self.root.insert(0, node)
            print self.root.find('xml_version')
        else:
            'setting xml_version'
            node.text = '2.0'

    def action_change_node_tag(self, node, new_tag):
        '''Change node tag'''
        node.tag = new_tag

    def action_change_node_text(self, node, new_text):
        '''Change node text'''
        node.text = new_text

    def action_change_submodel_id(self, submodel_node):
        '''Change child node <submodel_id> into an argument'''
        id_ = submodel_node.find('submodel_id').text
        submodel_node.set('submodel_id', id_ or '-2')
        submodel_node.remove(submodel_node.find('submodel_id'))

    def action_tag_to_name(self, node, change_to_tag):
        '''Change node tag and set "name" attribute'''
        node.set('name', node.tag)
        node.tag = change_to_tag

    def action_move_node(self, node, new_parent_path_or_node, extended_path = ''):
        '''Move node'''
        if isinstance(new_parent_path_or_node, str):
            parent_node = self.root.find(new_parent_path_or_node)
        else:
            parent_node = new_parent_path_or_node
        if extended_path:
            parent_node = parent_node.find(extended_path)
        if parent_node is None:
            raise ValueError('Could not move node %s because given parent path (%s) is not valid.' %
            (node.get('name', node.tag), new_parent_path_or_node))
        parent_node.insert(len(parent_node.getchildren()), node)

    def action_create_node(self, node_tag, node_attrib_dict, parent_node_path):
        '''Create new node'''
        node = etree.Element(node_tag, node_attrib_dict)
        if isinstance(parent_node_path, str):
            parent_node = self.root.find(parent_node_path)
        else:
            parent_node = parent_node_path
        if parent_node is None:
            self.warnings.append('Warning: Could not create node %s because the requested parent node (%s) was not found'
            %(node_tag, parent_node_path))
            return
        parent_node.insert(0, node)

    def action_delete_node(self, node):
        '''Delete redundant node'''
        node.getparent().remove(node)

    def action_delete_all_nodes_named(self, node, child_node_name):
        '''Delete redundant nodes with given names'''
        child_nodes = node.findall(child_node_name)
        for node_to_delete in child_nodes:
            node.remove(node_to_delete)

    def action_convert_selectable_list_node(self, selectable_list_node):
        '''Convert node into new <selectable> format'''
        selectable_list_node.set('name', selectable_list_node.tag)
        selectable_list_node.tag = 'selectable'
        selectable_list_node.set('type', 'selectable')
        # the only skip option currently known is 'Skip'
        text = 'True' if selectable_list_node.text != 'Skip' else 'False'
        if 'choices' in selectable_list_node.attrib:
            del selectable_list_node.attrib['choices']
        selectable_list_node.text = text

    def check_version(self):
        '''
        If the xml doesn't have a version number, or has an invalid one -- fix it and return 0.0
        as the version number. Otherwise just return the version number.
        '''
        current_version = 0.0
        version_node = self.root.find('xml_version')
        if version_node is None:
            self.add_action(self.action_update_version, None)
        else:
            try:
                current_version = float(version_node.text)
            except ValueError: # invalid version node, update it
                self.add_action(self.action_delete_node, version_node)
                self.add_action(self.action_update_version, None)
            self.add_action(self.action_update_version, version_node)
        return current_version

    def check_general(self):
        general = self.root.find('general')
        if general is None: return
        expr_lib = general.find('expression_library')
        if expr_lib is not None:
            variables = [n for n in expr_lib if n.get('type') == 'variable_definition']
            for variable_node in variables:
                self.tag_name_fix(variable_node, 'variable')

    def check_results_manager_indicator_batches(self, res_mgr):
        ib_node = res_mgr.find('Indicator_batches')
        if ib_node is None:
            return
        self.add_action(self.action_change_node_tag, ib_node, 'indicator_batches')
        self.add_action(self.action_change_node_attrib, ib_node, {'name': 'Indicator Batches'})
        # A list of tags in visualizations that should not be converted to <setting> tags
        NON_SETTING_TAGS = ['indicators', 'output_type', 'dataset_name', 'visualization_type']
        # tag fix batches and their viz
        for batch_node in ib_node.findall(".//*[@type='indicator_batch']"):
            for viz_node in batch_node.findall(".//*[@type='batch_visualization']"):
                has_settings = viz_node.find('settings') is not None
                for viz_child_node in viz_node:
                    if viz_child_node.tag not in NON_SETTING_TAGS:
                        if not has_settings:
                            self.add_action(self.action_create_node, None, 'settings', {}, viz_node)
                            has_settings = True
                        self.add_action(self.action_move_node, viz_child_node, viz_node, 'settings')
                        self.add_action(self.action_change_node_attrib, viz_child_node, {'hidden': None, 'type': None})
                        self.tag_name_fix(viz_child_node, 'setting')
                    else:
                        self.add_action(self.action_change_node_attrib, viz_child_node, {'hidden': None, 'type': None})
                self.tag_name_fix(viz_node, 'batch_visualization')
            self.tag_name_fix(batch_node, 'indicator_batch')

    def check_results_manager(self):
        res_mgr = self.root.find('results_manager')
        if res_mgr is None:
            return

        self.check_results_manager_indicator_batches(res_mgr)

        simruns_node = res_mgr.find('Simulation_runs')
        if simruns_node is not None:
            self.add_action(self.action_change_node_tag, simruns_node, 'simulation_runs')
            self.add_action(self.action_change_node_attrib, simruns_node, {'name': 'Simulation Runs'})
            for run_node in simruns_node.findall(".//*[@type='source_data']"):
                self.tag_name_fix(run_node, 'run')
                # clear out all hidden flags for child nodes and set runs node to hidden=Children
                for child_node in run_node.getchildren():
                    # hidden is not necessary as the run has a hidden='Children'
                    if child_node.get('hidden') is not None:
                        self.add_action(self.action_change_node_attrib, child_node, {'hidden':None})
                    # change run_id from a child node into an attribute
                    if child_node.tag == 'run_id':
                        self.add_action(self.action_change_node_attrib, run_node, {'run_id': child_node.text})
                        self.add_action(self.action_delete_node, child_node)
                    if child_node.tag in ('start_year', 'end_year') and not child_node.get('type') == 'integer':
                        self.add_action(self.action_change_node_attrib, child_node, {'type':'integer'})
                self.add_action(self.action_change_node_attrib, run_node, {'hidden':'Children'})
                # run name is now the attribute name=".."
                self.add_action(self.action_delete_all_nodes_named, run_node, 'run_name')


    def check_scenario_manager(self):
        scenario_mgr = self.root.find('scenario_manager')
        if scenario_mgr is None:
            return
        scenarios = [n for n in scenario_mgr if n.get('type') == 'scenario']
        for scenario_node in scenarios:
            self.tag_name_fix(scenario_node, 'scenario')

    def check_model_manager(self):
        # ensure that all model templates are under <templates> and that estimation_config is
        # under model_manager root. Also make sure that model_system is renamde to models
        mmgr = self.root.find('model_manager')
        if mmgr is None:
            return
        model_system = mmgr.find('model_system')
        if model_system is None:
            return

        template_nodes = model_system.findall(".//*[@type='model_template']")
        model_nodes = model_system.findall(".//*[@type='model']")
        estimation_config = model_system.find('estimation_config')

        if mmgr.find('templates') is None:
            atr = {'name': 'Model Templates', 'hidden':'True', 'parser_action': 'skip'}
            self.add_action(self.action_create_node, None, 'templates', atr, 'model_manager')
        if mmgr.find('models') is None:
            atr =  {'hidden':'False', 'name': 'Models', 'setexpanded': 'True',
                    'config_name': 'model_system', 'type': 'dictionary'}
            self.add_action(self.action_create_node, None, 'models', atr, 'model_manager')

        if estimation_config is not None:
            self.add_action(self.action_move_node, estimation_config, 'model_manager')
            self.add_action(self.action_change_node_attrib, estimation_config,
                            {'name': 'Estimation Configuration', 'config_name': 'estimation_config'})

        for template_node in template_nodes:
            self.check_model_spec(template_node)
            self.check_model_struct(template_node)
            self.tag_name_fix(template_node, 'model_template')
            self.add_action(self.action_move_node, template_node, 'model_manager/templates')
        for model_node in model_nodes:
            self.check_model_spec(model_node)
            self.check_model_struct(model_node)
            self.tag_name_fix(model_node, 'model')
            self.add_action(self.action_move_node, model_node, 'model_manager/models')

        self.add_action(self.action_delete_node, model_system)

    def check_model_struct(self, model_node):
        model_name = model_node.get('name', model_node.tag)
        struct_node = model_node.find('structure')
        if struct_node is None:
            return
        API_METHODS = ('run', 'init', 'prepare_for_run', 'prepare_for_estimate', 'estimate',
                       'group_by_attribute')
        for method_node in struct_node:
            method_name = (method_node.get('name') or method_node.tag)
            # import is a special case of methods
            if method_name == 'import':
                # fix class nodes
                for child_node in method_node:
                    if child_node.tag == 'classname':
                        self.add_action(self.action_change_node_tag, child_node, 'class_name')
                    elif child_node.tag == 'module':
                        self.add_action(self.action_change_node_tag, child_node, 'class_module')
                    else:
                        self.add_action(self.action_change_node_tag, child_node, 'argument')
                self.tag_name_fix(method_node, 'import')
            # only fix methods that are part of the API
            if method_name not in API_METHODS:
                self.warnings.append('%s has a structure node that is not part of the API (%s)' %
                                     (model_name, method_name))
                continue
            # self.tag_name_fix(method_node, method_node.tag)
            for argument_node in method_node:
                # catch the malplaced "models_to_run"
                if method_name == 'prepare_for_estimate' and argument_node.get('name', argument_node.tag) == 'models_to_run':
                    if model_node.find('estimation_config') is None:
                            self.add_action(self.action_create_node, None,
                                    'estimation_config',
                                    {'name': 'Estimation Configuration', 'parser_action': 'skip'},
                                    model_node)
                    self.add_action(self.action_change_node_tag, argument_node, 'config_override')
                    attribs = {'name': 'Models to run before estimation',
                              'config_name': 'models',
                              'parser_action': None}
                    self.add_action(self.action_change_node_attrib, argument_node, attribs)

                    self.add_action(self.action_move_node, argument_node,
                                    self._path_to_node(model_node) + '/estimation_config')
                    continue
                # messy node -> clean argument
                should_be_tag = 'argument' if not argument_node.tag in ('name', 'output') else argument_node.tag
                self.tag_name_fix(argument_node, should_be_tag)
                # dig down one level to fix tags in dictionary arguments
                for child_node in argument_node:
                    self.tag_name_fix(child_node, 'key')

    def check_model_spec(self, model_node):
        spec_node = model_node.find('specification')
        if spec_node is None:
            return
        # check for nodes that are not submodels and assume they are submodel groups
        group_nodes = [n for n in spec_node if n.get('type') != 'submodel']
        submodels = [n for n in spec_node if n.get('type') == 'submodel']
        for group_node in group_nodes:
            if group_node.get('type') != 'submodel_group':
                self.add_action(self.action_change_node_attrib, group_node, {'type': 'submodel_group'})
            self.tag_name_fix(group_node, 'submodel_group')
            # also convert submodels under the groups
            submodels.extend(node for node in group_node)
        for submodel_node in submodels:
            self.tag_name_fix(submodel_node, 'submodel')
            subid = submodel_node.find('submodel_id')
            if subid is not None:
                self.add_action(self.action_change_submodel_id, submodel_node)
            self.action_change_node_attrib(submodel_node, {'hidden': 'Children'})
            for equation_node in submodel_node.findall("*[@type='submodel_equation']"):
                self.tag_name_fix(equation_node, 'equation')
                eq_id_node = equation_node.find('equation_id')
                if eq_id_node is not None:
                    self.add_action(self.action_change_node_attrib, equation_node, {'equation_id': eq_id_node.text})
                    self.add_action(self.action_delete_node, eq_id_node)

    def check_selectable_lists(self):
        selectable_lists = self.root.findall(".//*[@type='selectable_list']")
        for selectable_list in selectable_lists:
            for selectable_node in selectable_list:
                if selectable_node.tag != 'selectable':
                    self.add_action(self.action_convert_selectable_list_node, selectable_node)

    def check_boolean_choices(self):
        # strip the redundant 'choices' attribute from all boolean choices
        boolean_nodes = self.root.findall(".//*[@type='boolean']")
        for boolean_node in boolean_nodes:
            if 'choices' in boolean_node.attrib:
                self.add_action(self.action_change_node_attrib, boolean_node, {'choices':None})

    def check_qouted_type(self):
        # type='quoted_string' should be type='string' parser_action='quote_string'
        # if the node already has a parser_action that is set to 'blank_to_None', add the attribute
        # empty_value_to_none='True'
        for node in self.root.findall(".//*[@type='quoted_string']"):
            attribs = {'type': 'string', 'parser_action': 'quote_string'}
            self.add_action(self.action_change_node_attrib, node,  attribs)

    def check_parser_action_blank_to_none(self):
        for node in self.root.findall(".//*[@parser_action='blank_to_None']"):
            attribs = {'parser_action': None, 'convert_blank_to_none': 'True'}
            self.add_action(self.action_change_node_attrib, node, attribs)

    def check_copyable_type(self):
        nodes_with_copyable_attribute = self.root.findall(".//*[@copyable]")
        for node in nodes_with_copyable_attribute:
            self.add_action(self.action_change_node_attrib, node, {'copyable':None})

    def check_tool_file(self, tool_node):
        # the name subchild is (was) what the module is called
        name_node = tool_node.find('name')
        if name_node is not None:
            self.add_action(self.action_change_node_tag, name_node, 'class_module')
        params = tool_node.find('params')
        if params is not None:
            for param_node in params:
                self.tag_name_fix(param_node, 'param')
                required_node = param_node.find('required')
                param_type_node = param_node.find('type')
                default_value_node = param_node.find('default')
                if required_node is not None:
                    is_required = 'True' if required_node.text == 'Required' else 'False'
                    self.add_action(self.action_change_node_attrib, param_node, {'required': is_required})
                    self.add_action(self.action_delete_node, required_node)
                if param_type_node is not None:
                    param_type = str(param_type_node.text or '').strip()
                    self.add_action(self.action_change_node_attrib, param_node, {'param_type': param_type})
                    self.add_action(self.action_delete_node, param_type_node)
                if default_value_node is not None:
                    self.add_action(self.action_change_node_text, param_node, default_value_node.text)
                    self.add_action(self.action_delete_node, default_value_node)

    def check_data_manager(self):
        data_mgr = self.root.find('data_manager')
        if data_mgr is None:
            return

        tool_lib_node = data_mgr.find('Tool_Library')
        if tool_lib_node is not None:
            self.add_action(self.action_change_node_tag, tool_lib_node, 'tool_library')
            tool_group_nodes = tool_lib_node.findall(".//*[@type='tool_group']")
            tool_file_nodes = tool_lib_node.findall(".//*[@type='tool_file']")
            tool_path_node = tool_lib_node.find('tool_path')
            if tool_path_node is not None:
                self.add_action(self.action_move_node, tool_path_node, 'data_manager')
                self.add_action(self.action_change_node_tag, tool_path_node, 'path_to_tool_modules')
                self.add_action(self.action_change_node_attrib, tool_path_node, {'hidden': None})
            for node in tool_group_nodes:
                self.tag_name_fix(node, 'tool_group')
            for node in tool_file_nodes:
                self.tag_name_fix(node, 'tool')
                self.check_tool_file(node)

        # tool sets have 'configs', which are alternative configurations for some existing
        # tool. Every node under a config that has no type is to be considered a parameter override
        tool_sets_node = data_mgr.find('Tool_Sets')
        if tool_sets_node is not None:
            self.add_action(self.action_change_node_tag, tool_sets_node, 'tool_sets')
            tool_set_nodes = tool_sets_node.findall(".//*[@type='tool_set']")
            for tool_set_node in tool_set_nodes:
                self.tag_name_fix(tool_set_node, 'tool_set')
                for tool_config_node in tool_set_node.findall("./*[@type='tool_config']"):
                    self.tag_name_fix(tool_config_node, 'tool_config')
                    param_nodes = [n for n in tool_config_node if n.get('type') is None]
                    for param_node in param_nodes:
                        self.tag_name_fix(param_node, 'param')

        # since tools never end up in configurations we can safely strip the 'types' attribute from
        # all tool related nodes
        for node in data_mgr.findall('.//*[@type]'):
            self.add_action(self.action_change_node_attrib, node, {'type': None})

    def check_class_type_nodes(self):
        class_type_nodes = self.root.findall(".//*[@type='class']")
        for class_type_node in class_type_nodes:
            cls_name_node = class_type_node.find('Class_name')
            cls_path_node = class_type_node.find('Class_path')
            if cls_name_node is not None:
                self.add_action(self.action_change_node_tag, cls_name_node, 'class_name')
            if cls_path_node is not None:
                self.add_action(self.action_change_node_tag, cls_path_node, 'class_module')
            for child_node in class_type_node.getchildren():
                # avoid converting special tags to arguments
                if child_node.tag not in ['Class_name', 'class_name', 'class_module', 'Class_path']:
                    self.tag_name_fix(child_node, 'argument')

    def open_xml_file(self, filename):
        tree = cElementTree.parse(filename)
        self.root = etree.fromstring(cElementTree.tostring(tree.getroot()))

    def complete_check(self, filename = None):
        # move submodel_id of submodels into an attribute
        if filename:
            self.open_xml_file(filename)

        # section checks
        current_version = self.check_version()
        # exit if the version is too high
        if current_version >= 2.0:
            msg = ('The XML reports to be of version %s, this tool only upgrades to version %s, so '
                   'no changes will occur.\n'
                   'If you want to to force an upgrade, remove the xml_version tag from the xml '
                   'file and run this tool again.'
                   %(current_version, "2.0"))
            self.write(msg)
        else:
            # manager checks
            self.check_general()
            self.check_model_manager()
            self.check_scenario_manager()
            self.check_data_manager()
            self.check_results_manager()
            # global checks
            self.check_selectable_lists()
            self.check_class_type_nodes()
            self.check_boolean_choices()
            self.check_parser_action_blank_to_none() # this MUST be before check_quoted_types
            self.check_qouted_type()

if __name__ == '__main__':
    import sys
    import os.path
    from optparse import OptionParser
    #set up command-line options
    usage = '%s [options] FILENAME' % sys.argv[0]
    parser = OptionParser(usage = usage)
    parser.add_option("-v", "--verbose",
            help="Verbose mode. Print changes to individual nodes.", default = False, action = "store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
            help="Quiet mode. Don't print changes to stdout (this option takes precedence over verbose mode)",
            default = False, action = "store_true", dest="quiet")
    parser.add_option("-d", "--dry-run",
            help="Only list changes, don't write anything to disk", default = False, action="store_true", dest="dry_run")
    parser.add_option("-o", "--outfile",
            help="Write changes to OUTFILE", dest="outfile")
    parser.add_option("-f", "--force",
            help="Do not ask about overwriting existing files", default = False, action = "store_true", dest="force")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(1)
    filename = args[0]
    # ensure we got a valid filename from the user
    valid_file = False
    if not os.path.exists(filename):
        print 'File "%s" does not exists' % filename
    elif not os.path.isfile(filename):
        print '"%s" is not a file' % filename
    else:
        valid_file = True
    if not valid_file:
        sys.exit(1)

    try:
        c = Converter(quiet = options.quiet, verbose = options.verbose)
        c.open_xml_file(filename)
        c.complete_check()
        c.execute()
    except SyntaxError, ex:
        print '\nSyntax Error while parsing file %s.\n%s\n' % (filename, ex)
    except IOError, ex:
        print '\nFile Error while parsing file %s.\n%s' % (filename, ex)
    # except Exception, ex:
    #     print '\nUnexpected Error while reading the file.\n%s' % ex
    finally:
        pass
    try:
        if options.dry_run:
            sys.exit(1)
        tree = etree.ElementTree(c.root)
        outfile = filename if options.outfile is None else options.outfile
        if os.path.exists(outfile) and not options.force:
            overwrite = ''
            while overwrite.lower() not in ['y', 'n', 'yes', 'no']:
                try:
                    overwrite = raw_input('The file "%s" already exists. Overwrite? (y/n): ' % outfile)
                except KeyboardInterrupt:
                    overwrite = 'n'
            if overwrite in ['n', 'no']:
                sys.exit(1)
        try:
            tree.write(outfile)
            print 'Wrote changes to %s' %outfile
        except Exception, ex:
            print 'An error occured while trying to save the file. Changes not saved.\n%s' % ex
    finally:
        pass
