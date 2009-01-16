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

from PyQt4.QtCore import SIGNAL, QString
from PyQt4.QtXml import QDomDocument, QDomNode

from opus_core.tests import opus_unittest

class XmlManipulator(object):
    '''Access and manipulation methods for dealing with PyQt XML objects'''

    def __init__(self, xml_controller):
        self._controller = xml_controller
        self._model = xml_controller.model
        self._view = xml_controller.view
        self._dom_document = self._model.domDocument

        self._absolute_xml_root = self._dom_document.documentElement()
        self.xml_version = self._model.mainwindow.toolboxBase.\
            opus_core_xml_configuration.xml_version


#    ==========================================
#     PRIVATE METHODS
#    ==========================================


    def _resolve_root_node(self, root):
        '''try to resolve argument to a dom node'''
        resolved_root = None
        if root is None:
            resolved_root = self._absolute_xml_root
        elif isinstance(root, QDomNode):
            if not root.isElement():
                resolved_root = None
            else:
                resolved_root = root.toElement()
        else:
            resolved_root = self.get(root, None)

        if not resolved_root:
            print 'Warning: Could not resolve root from %s' %str(root)
        return resolved_root

# TODO: create a test case for this
    def _hidden(self, element):
        '''returns true if the given element is hidden (has hidden=True)'''
        # check if this is hidden
        if element is None or element.isNull():
            return False
        # check if any nodes above this one is hidden (makes this hidden too)
        if self._hidden(element.parentNode()):
            return True
        # finally check if this one is actually hidden
        return self.get_attrib('hidden', element) and \
                self.get_attrib('hidden', element).lower() == 'true'


    def _get_child_text_node(self, element):
        '''search the child nodes of the element for a text node and return it
        or None if no such nodes was found'''
        child_nodes = element.childNodes()
        for x in xrange(0, child_nodes.length()):
            if child_nodes.item(x).isText():
                return child_nodes.item(x)
        return None


    def _item_for_element(self, element):
        '''determine the item for a given element node by reverse lookup.
        return None if one could not be found'''
        if element is None or element.isNull():
            return None
        # check if this is the root
        root_item = self._model._rootItem
        if element == root_item.node():
            return root_item

        # check if we can get the parent item
        parent_item = self._item_for_element(element.parentNode())
        if not parent_item is None:
            # locate this elements item in parents childItems
            for child in parent_item.childItems:
                if child.node() == element:
                    return child
            return None # could not find element in childs
        return None # no parent item found


    def _item_to_index(self, item):
        '''convert a given item to a QModelIndex()'''
        if item is None:
            return None
        return self._model.createIndex(item.row(), 0, item.parent())


    def _valid_tagname(self, tagname):
        '''check that tagname is a valid tag name for a xml node
        otherwise print a warning message'''
        if not self._model.validateTagName(tagname):
            print 'Warning: "%s" is not valid as tag name or attribute' %tagname
            return False
        return True



#    ==========================================
#     PUBLIC METHODS
#    ==========================================


    def manager_root(self):
        '''
        Return the manager root element (QDomElement) for the xml controller
        that holds this XmlManipulator instance.
            For example: models_manager.xml_controller.xml.manager_root()
            returns the root xml element for the Models Manager tab.
        '''
        return self._model.xmlRoot


    def get(self, element_or_path, root = None):
        '''
        Lookup for QDomElements. [element_or_path] is either the tag for the
        element to fetch, or a path to that element (including the tag).
        The path (and tag) is relative to [root]. If [root] is None, the
        absolute root of the project is used.
        '''
        root = self._resolve_root_node(root)
        if root is None:
            return None

        # grab the subtree element and return it
        path_steps = element_or_path.split('/')
        current_element = root

        while path_steps:
            sub_path = path_steps.pop(0)
            if sub_path:
                current_element = current_element.firstChildElement(sub_path)
                if current_element.isNull():
                    # could not resolve path all the way
                    return None

        return current_element


    def get_attrib(self, attribute_name, element):
        '''
        Returns the value (as a string) of attribute [attribute_name] from
        [element]. If no such attribute or element exists, the method returns
        None.
        '''
        if not element.hasAttribute(attribute_name):
            return None
        return element.attribute(attribute_name)


    def get_all(self, tag_or_attrib_dict, root_or_tuple):
        '''
        Get a tuple of all QDomElements that matches the criteria in
        [tag_or_attrib_dict]. If [tag_or_attrib_dict] is a string, matches are
        based on tag names. If it's a dictionary matches are based on attributes
        In the latter, dictionary keys are used for attribute names and
        dictionary values are used for attributes values.
        if [root_or_tuple] is a QDomNode, the child nodes of it is used as list
        to look for matches. If [root_or_tuple] is a tuple, it is assumed to
        contain a list of QDomElement to match against.
        '''
        elements = root_or_tuple
        if isinstance(elements, list):
            elements = tuple(elements)
        # if the root_or_tuple was not tuple or list, assume its a root element
        # and use a tuple of it's children
        if not isinstance(elements, tuple):
            elements = self.children(self._resolve_root_node(root_or_tuple))

        # match by tag name?
        if not isinstance(tag_or_attrib_dict, dict):
            return tuple([e for e in elements if \
                          e.tagName() == tag_or_attrib_dict])
        # match by attributes!
        matchlist = []
        for element in elements:
            add_this_element = True
            # test for complete attribute matching
            for attribute, value in tag_or_attrib_dict.items():
                if element.attribute(attribute) != value:
                    add_this_element = False
                    break
            if add_this_element:
                matchlist.append(element)
        return tuple(matchlist)


    def get_text(self, element, strip_white_space = True):
        '''
        Get the text value for [element].
        If [strip_white_space] is True, the leading and trailing whitespace is
        removed from the text before it's returned.
        '''
        # iterate over all the child elements and return the first text value
        text_node = self._get_child_text_node(element)
        if text_node:
            if strip_white_space:
                return text_node.nodeValue().trimmed()
            return text_node.nodeValue()
        return None


    def set_attrib(self, attrib_dict, element_or_tuple_of_elements):
        '''
        Sets attributes of elements. If [element_or_tuple_of_elements] is a
        list (or tuple), it is assumed to be a list of QDomElement for which to
        set the attributes in [attrib_dict]. The method also accepts a single
        QDomElement as [element_or_tuple_of_elements].
        '''
        # make sure we have a tuple
        if not isinstance(element_or_tuple_of_elements, (list, tuple)):
            element_or_tuple_of_elements = (element_or_tuple_of_elements,)
        for element in element_or_tuple_of_elements:
            for attribute, value in attrib_dict.items():
                if self._valid_tagname(attribute):
                    element.setAttribute(attribute, str(value))
            # since we modified the element, make it part of this project
            self._model.makeEditable(element)
        # make sure that the data is marked as dirty if appropriate
        if element_or_tuple_of_elements:
            self._controller.model.markAsDirty()


    def set_text(self, text, element_or_tuple_of_elements):
        '''
        Set the text value of an element to [text]
        If [element_or_tuple_of_elements] is a list or tuple, it's assumed to
        be a list of QDomElement and the text value is set for each of them.
        The method also accepts a single QDomElement as
        [element_or_tuple_of_elements].
        '''
        element_tuple = element_or_tuple_of_elements
        if not isinstance(element_tuple, (list, tuple)):
            element_tuple = (element_tuple,)
        if text is None:
            text = ''
        if not isinstance(text, (QString, str)):
            print('Warning: Got non string argument to set_text(). \n'
                  'Converted value is "%s"'%(str(text)))
            text = str(text)

        for element in element_tuple:
            text_node = self._get_child_text_node(element)
            if not text_node: # insert new text as first child
                text_node = self._dom_document.createTextNode(text)
                element.insertBefore(text_node, QDomNode())
            else:
                text_node.setNodeValue(text)
            # add to project
            self._model.makeEditable(element)
        # make sure that the data is marked as dirty
        if element_tuple:
            self._controller.model.markAsDirty()


    def children(self, element = None):
        '''
        Return a tuple consisting of all child QDomElement's of [element].
        If [element] is None, the absolute root of the project is used.
        '''
        childlist = []
        element = self._resolve_root_node(element)
        if element is None:
            return tuple()
        child = element.firstChildElement()
        while not child.isNull():
            childlist.append(child)
            child = child.nextSiblingElement()
        return tuple(childlist)


    def create(self, tagname, root = None, update_gui=True, first_item = True):
        '''
        Creates a new QDomElement named [tagname] and inserts it under [root]
        If root is None, the absolute root for the project is used
        If update_gui is True the GUI is forced to update the subtree of [root]
            Note: This is very slow if it is done many times and/or
            for a large subtree. If you find the insertion to be slow, pass
            update_gui as False, do all insertions and then use refresh([root])
        If first_item is True the new element is inserted directly under [root]
        '''
        root = self._resolve_root_node(root)
        if root is None:
            return None
        # make sure name is valid
        if not self._valid_tagname(tagname):
            return None
        spawn = self._dom_document.createElement(tagname)
        if first_item:
            root.insertBefore(spawn, QDomNode())
        else:
            root.appendChild(spawn)
        # make the item a part of this project if inherited
        self._model.makeEditable(spawn)
        # insert tree under root
        item = self._item_for_element(root)
        if not item is None and update_gui is True:
            item.refresh()
            self._model.emit(SIGNAL('layoutChanged()'))
        # mark model as dirty since we changed it's data
        self._controller.model.markAsDirty()
        return spawn


    def delete(self, element):
        '''Deletes [element] (and all it's child nodes) and updates the GUI.'''
        # removing inherited nodes messes things up
        if not self.get_attrib('inherited', element) is None:
            print "Warning: Can't remove inherited elements"
            return
        # for hidden nodes, we remove it manually
        # visible nodes must go through the models remove row
        if self._hidden(element):
            element.parentNode().removeChild(element)
            # mark model as dirty since we changed it's data
            self._controller.model.markAsDirty()
        else:
            # locate item by reverse lookup from element and delete row
            item = self._item_for_element(element)
            parent_index = self._item_to_index(item)
            self._model.removeRow(item.row(), parent_index)


    def rename(self, tagname, element):
        '''
        Renames the tag for [element] to [tagname] if the [tagname] is a
        valid XML tag name
        '''
        if not self._valid_tagname(tagname):
            return
        element = element.toElement()
        if not element.isNull():
            element.setTagName(tagname)
            self._model.makeEditable(element)
            # mark model as dirty since we changed it's data
            self._controller.model.markAsDirty()
        else:
            print 'Could not rename node %s' %element


    def selected(self):
        '''
        Get the currently selected element in the Manager Tree Widget or None
        if no item is selected.
        '''
        selected = self._view.currentIndex()
        if not selected.isValid():
            return None
        selected = selected.internalPointer().node().toElement()
        if selected.isNull():
            return None
        return selected


    def element_at(self, position):
        '''
        Get the QDomElement at position (QPoint)
        Use in methods callback methods such as processCustomMenu where the
        argument is a QPoint.
        '''
        selected = self._view.itemAt(position)
        if not selected.isValid():
            return None
        selected = selected.internalPointer().node().toElement()
        if selected.isNull():
            return None
        return selected


    def refresh(self, element = None):
        '''
        Forces the GUI to reinsert element and all each item in it's entire
        subtree. If element is None, the manager root is used (manager_root()).
        '''
        if element is None:
            element = self.manager_root()
        item = self._item_for_element(element)
        if item is None:
            return
        item.refresh()
        self._model.emit(SIGNAL('layoutChanged()'))



class XmlManipulatorTester(opus_unittest.OpusTestCase):

    xml = '''
        <opus_project>
          <levelone>
            <child1 type="a_type" attrib="an_attrib">
            </child1>
            <child2>
              <child3/>
            </child2>
          </levelone>
          <leveltwo type="test">sole text
          </leveltwo>
          <levelthree type="test" hidden="True">
              text and nodes
              <get_me></get_me>
              <get_me></get_me>
              <get_me></get_me>
          </levelthree>
        </opus_project>
    '''

    def _tuple_to_tagnames(self, element_tuple):
        '''helper method to both test for correct type (tuple)
        and convert a sequence of elements to a sequence of tagnames'''
        if not isinstance(element_tuple, tuple):
            raise TypeError('Error: Should have got tuple.')
        return tuple([e.tagName() for e in element_tuple])

    def _restore_xml_tree(self):
        '''restore the test xml tree to original state'''
        self.xml._dom_document = self.original_doc_tree.cloneNode(True)

    def setUp(self):
        from opus_gui.abstract_manager.models.xml_item import XmlItem
        from opus_core.configurations.xml_configuration import XMLVersion

        class Dummy: pass
        class DummyModel(object):
            def __init__(self, dd):
                self.mainwindow = Dummy()
                self.domDocument = dd
                tb = Dummy()
                tb.opus_core_xml_configuration = Dummy()
                tb.opus_core_xml_configuration.xml_version = XMLVersion('0.9')
                self.mainwindow.toolboxBase = tb
                self._rootItem = XmlItem(dd, dd.documentElement(), None)
                self._rootItem.initAsRootItem()
                self.xmlRoot = dd.documentElement().\
                    firstChildElement('leveltwo')
                self.markAsDirty = lambda: ()
            # create fake abstract model methods that are used
            def createIndex(self, row, col, parent): pass
            def removeRow(self, row, parent_node): pass
            def isTemporary(self): return False
            def beginRemoveRows(self, x, y, z): pass
            def endRemoveRows(self): pass
            def emit(self, x): pass
            def validateTagName(self,tag):
                from PyQt4.QtCore import QRegExp
                return QRegExp("[a-zA-Z_:][-a-zA-Z0-9._:]*").exactMatch(tag)
            def makeEditable(self, node): pass


        ctrl = Dummy()
        ctrl.view = None
        doc = QDomDocument()
        doc.setContent(self.xml)
        # backup original so we can restore it
        self.original_doc_tree = doc.cloneNode(True)
        ctrl.model = DummyModel(doc)

        self.root = doc.documentElement()
        self.xml = XmlManipulator(ctrl)


    def tearDown(self):
        pass


    def test_xml_version(self):
        self.assertEqual(self.xml.xml_version, '0.9')


    def test_get(self):
        # test implicit root
        self.assertEqual(self.xml.get('levelone'),
                         self.xml.get('levelone', self.root))

        # correct path handling, all of these should resolve to the same node
        one = self.xml.get('levelone/child1')
        lead = self.xml.get('/levelone/child1')
        lead_and_end = self.xml.get('/levelone/child1/')
        self.assertEqual(one, lead)
        self.assertEqual(lead, lead_and_end)
        # correct returns
        self.assertTrue(self.xml.get('i/dont/exist/') is None)
        self.assertTrue(self.xml.get('levelone', QDomNode()) is None)#false root
        self.assertTrue(self.xml.get('////complete_nonsense///') is None)


    def test_get_all(self):
        all_tests = self._tuple_to_tagnames(self.xml.get_all({'type':'test'},
                                                             self.root))
        self.assertEqual(all_tests, ('leveltwo', 'levelthree'))

        all_children = self._tuple_to_tagnames(self.xml.get_all({},
                                                                self.root))
        self.assertEqual(all_children, ('levelone', 'leveltwo', 'levelthree'))

        all_get_me = self._tuple_to_tagnames(self.xml.get_all('get_me',
                                                    self.xml.get('levelthree')))
        self.assertEqual(all_get_me, ('get_me', 'get_me', 'get_me'))


    def test_get_text(self):
        l1 = self.xml.get('levelone')
        l2 = self.xml.get('leveltwo')
        l3 = self.xml.get('levelthree')
        # no text --> none
        self.assertTrue(self.xml.get_text(l1) is None)
        # test for white space preserving
        self.assertEqual(self.xml.get_text(l2, False), 'sole text\n          ')
        # default should be to strip ws
        self.assertEqual(self.xml.get_text(l3), 'text and nodes')


    def test_set_text(self):
        e1 = self.xml.get('levelone')
        e2 = self.xml.get('leveltwo')
        e3 = self.xml.get('levelthree')
        # basic set
        self.xml.set_text('after', e2)
        self.assertEqual(self.xml.get_text(e2), 'after')
        # create node if none exist
        self.assertTrue(self.xml.get_text(e1) is None)
        self.xml.set_text('text', e1)
        self.assertEqual(self.xml.get_text(e1), 'text')
        # set all nodes to text
        self.xml.set_text('quick and easy', (e1, e2, e3))
        self.assertEqual(self.xml.get_text(e1), 'quick and easy')
        self.assertEqual(self.xml.get_text(e2), 'quick and easy')
        self.assertEqual(self.xml.get_text(e3), 'quick and easy')
        # set with non text argument
        self.xml.set_text(5, e1)

        self._restore_xml_tree()


    def test_delete(self):
        # must have functional model to test
        pass
#        self.assertFalse(self.xml.get('levelone') is None)
#        self.xml.delete(self.xml.get('levelone'))
#        self.assertTrue(self.xml.get('levelone') is None)

#        self._restore_xml_tree()


    def test_create(self):
        # creation works
        # creation does not work for non valid names
        # create doesn't work for invalid roots
        root = self.root
        created = self.xml.create('i_was_created', root, True, False)
        self.assertFalse(created is None)
        self.assertFalse(self.xml.get('i_was_created', root) is None)
        not_created = self.xml.create('invalid name', root, True, False)
        self.assertTrue(not_created is None)
        self.assertTrue(self.xml.get('invalid name', root) is None)
        self.assertTrue(self.xml.create('validname', QDomNode()) is None)

    def test_rename(self):
        l2 = self.xml.get('leveltwo')
        self.assertTrue(l2.tagName() == 'leveltwo')
        self.xml.rename('renamed', l2)
        self.assertTrue(l2.tagName() == 'renamed')

        self._restore_xml_tree()


    def test_set_attrib(self):
        some_attributes = {'a1':1, 'a2':('list', 'of', 'items'), 'a3':'string'}
        has_all_attributes = lambda x: \
                            x.attribute('a1') == '1' and \
                            x.attribute('a2') == "('list', 'of', 'items')" and \
                            x.attribute('a3') == 'string'
        l1 = self.xml.get('levelone')
        l2 = self.xml.get('leveltwo')
        # single element
        self.xml.set_attrib(some_attributes, l1)
        self.assertTrue(has_all_attributes(l1))
        # multiple elements at once
        self.xml.set_attrib(some_attributes, (l1, l2))
        self.assertTrue(has_all_attributes(l1))
        self.assertTrue(has_all_attributes(l2))

        self._restore_xml_tree()


    def test_get_attrib(self):
        l3 = self.xml.get('levelthree')
        atr_val = self.xml.get_attrib('type', l3)
        self.assertEqual(atr_val, 'test')
        self.assertTrue(self.xml.get_attrib('dontexist', l3) is None)


    def test_get_manager_root(self):
        # manager root for test object is set to be 'leveltwo'
        self.assertEqual(self.xml.manager_root().tagName(), 'leveltwo')


    def test_item_for_element(self):
        child2_item = self.xml._model._rootItem.childItems[0].childItems[1]
        child2_element = self.xml.get('levelone/child2')
        self.assertEqual(child2_item,
                         self.xml._item_for_element(child2_element))
        self.assertTrue(self.xml._item_for_element(QDomNode()) is None)
        # check that hidden nodes dont get returned as items
        hidden = self.xml.get('levelthree')
        self.assertTrue(self.xml._item_for_element(hidden) is None)

if __name__ == '__main__':
    opus_unittest.main()

