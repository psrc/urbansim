# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import copy

from lxml.etree import tostring

from opus_gui.main.controllers.instance_handlers import update_mainwindow_savestate
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.configurations.xml_configuration import node_identity_string, element_id
from opus_core.opus_exceptions.xml_version_exception import XMLVersionException

class OpusProject(object):
    '''
    Methods and attributes for handling an OPUS project file.
    Inheritance is done by letting a XmlConfiguration object handle loading and saving.
    Each project has two root nodes, one for the full tree and one for the tree of all inherited
    values. Nodes that exists in the full tree AND in the inherited tree, but with different values
    are called "shadowing nodes", since they shadow the inherited value with a local variation.
    '''
    def __init__(self):
        self.name = ''              # Project name
        self.filename = ''          # Filename of loaded project
        self.xml_config = None      # XMLController object
        self._root_node = None      # Full project tree root
        self._inherited_root = None # Root node of the tree with inherited nodes (original values)
        self._shadowing_nodes = {}  # Mapping of nodes in local tree to nodes in inherited tree
        self._dirty = False         # Dirty flag

    def __is_dirty(self):
        return self._dirty

    def __set_dirty(self, dirty):
        self._dirty = dirty
        update_mainwindow_savestate()

    dirty = property(__is_dirty, __set_dirty)

    def _read_xml_from_config(self, xml_config):
        ''' Extract XML information from the XML Configuration object '''
        self.xml_config = xml_config
        self._root_node = xml_config.full_tree.getroot()

        if xml_config.inherited_tree is None:
            self._inherited_root = XMLConfiguration().full_tree.getroot()
        else:
            self._inherited_root = xml_config.inherited_tree
        # map id's to nodes for the inherited and the local nodes
        inherited_ids_to_nodes = dict((node_identity_string(n), n) for
                                      n in self._inherited_root.getiterator())
        local_ids_to_nodes = dict((node_identity_string(n), n) for
                                  n in self._root_node.getiterator() if not n.get('inherited'))

        self._shadowing_nodes = {}
        # join the local and inherited nodes on id-match
        for id_, node in local_ids_to_nodes.items():
            if id_ in inherited_ids_to_nodes:
                self._shadowing_nodes[node] = inherited_ids_to_nodes[id_]

        if self.find('./general/project_name') is not None:
            self.name = self.find('./general/project_name').text
        else:
            self.name = 'unnamed_project'
        os.environ['OPUSPROJECTNAME'] = self.name
        self.dirty = False

    def open(self, filename):
        '''
        Load a project file from XML.
        @return: flag and message (tuple(boolean, String))
        The flag is only True if the project loaded without problems.
        '''
        # Always close the project before loading another one to avoid mixing
        # data if the load is only partly successful
        self.close()
        filename = str(filename)
        if not os.path.exists(filename):
            return (False, "Tried to load project from file '%s', but that file "
                    "does'nt exist" %filename)
        default_path = os.path.dirname(filename)
        filename = os.path.basename(filename)
        try:
            xml_config = XMLConfiguration(filename, default_path)
            self._read_xml_from_config(xml_config)
            self.filename = os.path.normpath(os.path.join(default_path, filename))
            return (True, 'Project %s loaded OK' % filename)
        # Catch only the errors that XMLConfiguration is known to throw
        except (IOError, SyntaxError, ValueError, SyntaxError, XMLVersionException), ex:
            self.close()
            return (False, str(ex))

    def save(self, filename = None):
        '''
        Save a project file to disk
        @param filename (String): filename to save under.
        If filename is None, the filename that the project loaded from is used.
        @return: flag and message (tuple(boolean, String)
        flag is only True if the file was successfully saved.
        '''
        if not self.is_open(): return

        if filename is None:
            filename = self.filename

        self.update_xml_config() # Converts current tree to ET and cleans the tree from temp data

        try:
            self.xml_config.save_as(filename)
        except IOError, ex:
            return (False, 'An error occurred when trying to save the project.\n'
                    'The error is described as: ' + str(ex))

        self.dirty = False
        return (True, 'Project successfully saved')

    def _add_to_shadowing_nodes(self, node):
        '''
        Convenience method to add a node to the shadow map with error checking
        @param node (Element) node to add to shadow map
        '''
        id_ = node_identity_string(node)
        inherited_node = self.find_by_id_string(id_, self._inherited_root)
        if inherited_node is not None:
            self._shadowing_nodes[node] = inherited_node

    def insert_node(self, node, parent_node, row = 0):
        '''
        Insert a node into the XML DOM tree. Can only insert nodes that are not already in the
        tree (identified by their id string).
        @param node (Element) node to insert (all child nodes are also inserted)
        @param parent_node (Element) the parent to attach the node to
        @param row (int) insert the new node as row:th child of parent_node
        @return the inserted node (Element) or None if the node was not inserted (already exists)
        '''
        # check if there are any nodes with this nodes id string
        future_id = node_identity_string(parent_node) + element_id(node)
        try:
            existing_node = self.find_by_id_string(future_id, parent_node.getroottree().getroot())
        except LookupError: # nodes with this id already exists
            return None
        if existing_node is not None:
            return None # don't allow overwriting existing nodes
        # Insert the node
        parent_node.insert(row, node)
        self.make_local(node)
        return node

    def delete_node(self, node):
        '''
        Delete a node from the XML DOM. If the node was shadowing an inherited node, the inherited
        node is (re-)inserted into the DOM and returned. Calling delete_node on an inherited node
        has no effect.
        @node (Element) node to remove
        @return the (re-inserted) node (Element) or None
        '''
        # The three cases of deleting a node:
        # The node is local (simplest case -- just remove it)
        # The node is inherited (no, wait, this is the simplest case -- do nothing)
        # The node is shadowing an inherited node (remove the node, insert the inherited copy)

        # helper function to clean out all child nodes from shadowing_nodes
        def clean_shadownodes(node):
            for child_node in node:
                clean_shadownodes(child_node)
            if node in self._shadowing_nodes:
                del self._shadowing_nodes[node]
        reinserted_node = None
        if node.get('inherited'):
            pass
        elif node in self._shadowing_nodes:
            inherited_node = copy.deepcopy(self._shadowing_nodes[node])
            clean_shadownodes(node)
            parent = node.getparent()
            node_index = parent.index(node)
            parent.remove(node)
            parent.insert(node_index, inherited_node)
            reinserted_node = inherited_node
        else:
            clean_shadownodes(node)
            parent = node.getparent()
            parent.remove(node)
        return reinserted_node

    def make_local(self, node):
        '''
        Make a node local to the current project. All parent nodes (but not their respective child
        nodes) are also made local as well as all child nodes of the given node.
        @node (Element) node to make local
        '''
        def localize_node(node):
            if node is self._root_node: return
            if node.get('inherited') is not None:
                del node.attrib['inherited']
                self._add_to_shadowing_nodes(node)
                self.dirty = True
        def localize_parents(node):
            if node is None: return
            localize_node(node)
            localize_parents(node.getparent())
        def localize_children(node):
            localize_node(node)
            map(localize_children, list(node))

        localize_parents(node.getparent())
        localize_children(node)

    def same_node_id(self, node1, node2, only_nodes = False):
        '''
        Checks the two nodes node1 and node2 are the same by identity (tag+name are identical for
        all nodes in their paths). If only_nodes is True, the two nodes are assumed to have
        identical paths and the test is only done for the two leaf nodes.
        '''
        if node1 is None and node2 is None:
            return True
        if (node1 is None and node2 is not None) or (node1 is not None and node2 is None):
            return False
        if not (node1.tag == node2.tag and node1.get('name') == node2.get('name')):
            return False
        if not only_nodes:
            return self.same_node_id(node1.getparent(), node2.getparent())
        return True

    def find_by_id_string(self, id_string, tree_root = None):
        '''
        Select a node by it's id string in a given tree (default tree is project root).
        @param id_string (str) the id string for the node to select
        @param tree_root (Element) root of the tree to insert node in
        @return the resolved node (Element) or None
        @raises LookupError if the id cannot be resolved to a single node
        @raises SyntaxError if the id_string format is incorrect
        '''
        def lookup_next(node, path_steps):
            step = path_steps[0]
            path_steps = path_steps[1:]
            try: tag, name = step.split(':')
            except ValueError:
                raise SyntaxError('id path contained invalid node reference. References should be in '
                                  'the format tag:name (name can be empty). Found for node: %s in %s' %
                                  (step, id_string))
            found_nodes = node.findall(tag)
            found_nodes = [node for node in found_nodes if (node.get('name') == name) or (name == '')]
            if len(found_nodes) > 1:
                raise LookupError('id path resolved to multiple nodes. Found %d nodes like %s (from %s)'
                                  % (len(found_nodes), step, id_string))
            if len(found_nodes) == 0:
                return None

            return lookup_next(found_nodes[0], path_steps) if path_steps else found_nodes[0]

        if tree_root is None:
            tree_root = self._root_node
        all_path_steps = id_string.split('/')
        # if there's no empty first we have a syntax error
        if all_path_steps[0] != '':
            raise SyntaxError('id path did not start with leading slash (/): %s' % id_string)
        all_path_steps = all_path_steps[1:]
        return lookup_next(tree_root, all_path_steps)

    def update_xml_config(self):
        '''
        Updates the XML Configuration object with the XML contents from this
        project.
        '''
        if self.is_open():
            self.xml_config.update(tostring(self._root_node))

    def close(self):
        ''' Close the project - removing any references to files or projects '''
        self.name = ''
        self.filename = ''
        self.xml_config = None
        self._root_node = None
        self.dirty = False
        self._shadowing_nodes = {}
        os.environ['OPUSPROJECTNAME'] = 'misc'

    def find(self, node_path, name = None, get_all = False):
        '''
        Wrapper for the find() method of the project root.
        Used mainly for code clarity as filtering on the name argument can be passed as an argument.
        @param node_path (str) path to the node to select
        @param name (str) name of the node to select
        @return the found element (Element) or None
        '''
        if self._root_node is None:
            return None
        if name is not None:
            return self._root_node.find(node_path + "[@name='%s']" % name)
        return self._root_node.find(node_path)

    def findall(self, node_path, name = None):
        '''
        Wrapper around the findall() method for the root element.
        @param node_path xpath expression for selecting nodes.
        @param name filter by nodes having attribute "name" set to the given name
        @return a list of all nodes matching node_path
        '''
        if self._root_node is None:
            return []
        if name is None:
            return self._root_node.findall(node_path)
        return self._root_node.findall(node_path + "[@name='%s']" % name)

    def is_open(self):
        '''
        Check if this is an open project
        @return True if there is a loaded project, False otherwise
        '''
        return self.xml_config is not None

    def is_shadowing(self, node):
        ''' Check if a node is shadowing an inherited value
        @param node (Element) node to check
        @return True if the node is shadowing an inherited value, otherwise False
        '''
        return node in self._shadowing_nodes

    def get_prototype_node(self, node):
        '''
        Returns the prototype node for a given node. If the node is shadowing an inherited node,
        returns the inherited node. If the node is local returns None. If the node is inherited
        returns itself.
        @param node (Element) the node to get inherited values for
        @return a copy of the inherited node (Element)
        '''
        if node.get('inherited') is not None:
            return node
        if self.is_shadowing(node):
            return copy.deepcopy(self._shadowing_nodes[node])
        return None

    def data_path(self):
        '''
        Get the project's data directory
        @return: Full path to project's data directory (String) or None if the
        project is not open.
        '''
        if not self.is_open():
            return None
        opus_data_path = self.xml_config.get_opus_data_path()
        return os.path.join(opus_data_path, self.name)

    def root_node(self):
        '''
        Get the project root node or None
        @return root node for project (Element) or None
        '''
        return self._root_node

