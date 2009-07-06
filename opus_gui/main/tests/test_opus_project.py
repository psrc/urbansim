# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.main.opus_project import *

from opus_core.tests import opus_unittest
from lxml.etree import Element, SubElement

class TestOpusProject(opus_unittest.OpusTestCase):
    ''' Test suite for Opus Project '''

    def setUp(self):
        # Validate that the test data is present
        self.testdatapath = os.path.split(__file__)[0]
        self.testdatapath = os.path.join(self.testdatapath, 'testdata')
        self.testfile_valid = os.path.join(self.testdatapath, 'project_valid.xml')
        self.testfile_invalid = os.path.join(self.testdatapath, 'project_invalid.xml')
        self.p = OpusProject()

    def _open(self, fn):
        fn = os.path.join(self.testdatapath, fn)
        ok, msg = self.p.open(fn)
        if not ok:
            print msg
        self.assertTrue(self.p.is_open())
        return self.p

    def project_is_closed(self, instance):
        '''
        Returns True of the project is closed
        '''
        set_to_default = True
        if 'OPUSPROJECTNAME' in os.environ:
            set_to_default = os.environ['OPUSPROJECTNAME'] == 'misc'

        return set_to_default and \
            (instance.name == '') and \
            (instance.filename == '') and \
            (instance.xml_config == None) and \
            (instance._root_node == None) and \
            (instance.dirty == False) and \
            (instance._shadowing_nodes == {})

    def test_close(self):
        ''' Make sure that the project closed up OK '''
        instance = self.p

        TESTVALUE = 'A TEST VALUE'

        instance.name = TESTVALUE
        instance.filename = TESTVALUE
        instance.xml_config = TESTVALUE
        instance._root_node = TESTVALUE
        instance.dirty = TESTVALUE

        # We also want to test that the environment variable 'OPUSPROJECTNAME'
        # is reset as it should, but need to be careful not to leave any side
        # effects from the test
        prev_environ = None
        if 'OPUSPROJECTNAME' in os.environ:
            prev_environ = os.environ['OPUSPROJECTNAME']
        os.environ['OPUSPROJECTNAME'] = TESTVALUE
        try:
            instance.close()
            self.assertTrue(self.project_is_closed(instance),
                            'Not all values were reset when the project was closed')
            self.assertFalse(instance.is_open())
        finally:
            if prev_environ is not None:
                os.environ['OPUSPROJECTNAME'] = prev_environ
            else:
                del os.environ['OPUSPROJECTNAME']

    def test_open(self):
        p = self.p
        flag, _ = p.open('__I__WONT__EXIST__')
        self.assertFalse(flag)
        flag, _ = p.open(self.testfile_invalid)
        self.assertFalse(flag)
        flag, msg = p.open(self.testfile_valid)
        self.assertTrue(flag)
        self.assertTrue(p.dirty is False)
        # Test that the XML is correct
        self.assertTrue(p.root_node().tag == 'opus_project')
        # Test that the find method is equivalent to using nodes find
        self.assertTrue(p.find('general/project_name') is p.root_node().find('general/project_name'))
        # Test that the name got parsed OK
        self.assertEquals(p.name, 'test_project')
        # Test that the data path is based on the name
        self.assertTrue(p.data_path().endswith(os.path.sep + 'test_project'))
        # Make sure no data is left arond when we open another file and fails
        p.open('__I__WONT__EXIST__')
        self.assertTrue(self.project_is_closed(p))

    def test_save(self):
        # TODO implement test for saving
        pass

    def test_data_path(self):
        # note: this only tests that the project name gets appended to the end
        p = self._open('child.xml')
        self.assertTrue(p.data_path().endswith('test'))

    def test_delete_node(self):
        # TODO need tests for deletion of nodes deeper than rootnode children
        p = self._open('child.xml')
        i_start = p.find('inherited')
        s_start = p.find('shadowing')
        l_start = p.find('local')
        # shadowing node should be only the three nodes: opus_project, general and shadowing
        self.assertTrue(s_start in p._shadowing_nodes)
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        self.assertEqual(len(p._shadowing_nodes), 3)

        # delete nodes and assert that nothing changes the inherited tree (orignal values for nodes)
        inherited_tree_start = tostring(p._inherited_root)
        ins_i = p.delete_node(i_start)
        self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
        ins_s = p.delete_node(s_start)
        self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
        ins_l = p.delete_node(l_start)
        self.assertEqual(inherited_tree_start, tostring(p._inherited_root))

        i_end = p.find('inherited')
        s_end = p.find('shadowing')
        l_end = p.find('local')

        self.assertTrue(i_start is i_end) # delete inherited should leave the node intact
        self.assertTrue(s_end.get('inherited') is not None)
        self.assertTrue(s_end.text == 'parent_value') # delete shadowing node reinserts inherited
        self.assertTrue(l_end is None) # deleting locals removes them
        # test that only removing shadowing nodes returns inserted nodes
        self.assertTrue(ins_i is None)
        self.assertTrue(ins_s is not None)
        self.assertTrue(ins_l is None)
        # check that the shadowing node was removed from the shadowing nodes map
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        # run multiple passes of making local and deleting inherited nodes -- some things vary
        # when doing this (like which nodes that are readded), so it's useful to test it
        for nth in range(1, 3):
            i = p.find('inherited')
            p.make_local(i)
            i_ins = p.delete_node(i)
            i = p.find('inherited')
            self.assert_(i_ins is i)
            self.assert_(i not in p._shadowing_nodes)
            s = 'pass #%d of make_local/delete_node failed' % nth
            self.assert_(i is not None, s)
            self.assert_(i.get('inherited') is not None, s)

    def test_find(self):
        p = self._open('find.xml')
        anode_default = p.find('node')
        anode_name = p.find('node', name = 'anode')
        no_node_with_that_name = p.find('node', name = 'not here')
        first_grandchild_by_name = p.find('node/node', name = 'grandchild')

        self.assertTrue(anode_default.get('name') == 'anode')
        self.assertTrue(anode_name is anode_default)
        self.assertTrue(no_node_with_that_name is None)
        self.assertEqual(first_grandchild_by_name.get('sparkles'), 'yep')

    def test_findall(self):
        p = self._open('find.xml')
        grandchildren = self.p.findall('node/node')
        named_grandchildren = self.p.findall("node/node", name='grandchild')
        self.assertEqual(len(grandchildren), 4)
        self.assertEqual(named_grandchildren[0].get('sparkles'), 'yep')
        self.assertEqual(named_grandchildren[1].get('sprinkles'), 'of course')

    def test_find_by_id_string(self):
        p = self._open('find.xml')
        proj_w_shadow = os.path.join(self.testdatapath, 'find.xml')
        p.open(proj_w_shadow)
        self.assertTrue(p.is_open())
        # selecting without names
        self.assertTrue(p.find_by_id_string('/general:/project_name:') is p.find('general/project_name'))
        # selecting with names
        self.assertTrue(p.find_by_id_string('/node:anode/node:grandchild') is p.find('node/node'))
        self.assertRaises(SyntaxError, p.find_by_id_string, 'mumbo jumbo')
        self.assertRaises(SyntaxError, p.find_by_id_string, 'node:anode/node:grandchild') # no leading slash
        self.assertRaises(LookupError, p.find_by_id_string, '/node:') # two of those
        self.assertTrue(p.find_by_id_string('/wontexist:') is None)

    def test_make_local(self):
        p = self._open('child.xml')
        # fc = first child, sc = second child
        fc = p.find('a/pretty/deep/path', name = 'first child')
        sc = p.find('a/pretty/deep/path', name = 'second child')
        self.assertTrue(fc.get('inherited') is not None)
        self.assertTrue(sc.get('inherited') is not None)
        # making first child local should not affect second child, only fc and all it's parents
        p.make_local(fc)
        n = p._root_node
        for path in ['a', 'pretty', 'deep', 'path']:
            n = n.find(path)
            self.assertTrue(n.get('inherited') is None)
            self.assertTrue(n in p._shadowing_nodes)
        self.assertTrue(sc.get('inherited') is not None)
        # making deep (parent of fc, and sc) should make both child nodes local
        p.make_local(p.find('a/pretty/deep'))
        self.assertTrue(fc.get('inherited') is None)
        self.assertTrue(sc.get('inherited') is None)
        self.assertTrue(fc in p._shadowing_nodes)
        self.assertTrue(sc in p._shadowing_nodes)

    def test_get_prototype_node(self):
        p = self._open('child.xml')
        local = p.find('local')
        shadowing = p.find('shadowing')
        inherited = p.find('inherited')
        self.assert_(p.get_prototype_node(local) is None)
        # prototype returns copy of inherited so do equality instead if instance check
        self.assertEqual(tostring(p.get_prototype_node(shadowing)),
                         tostring(p._inherited_root.find('shadowing')))
        self.assert_(p.get_prototype_node(inherited) is inherited)

    def test_insert_node(self):
        p = self._open('child.xml')

        new = Element('new_node')                                   # ok - new tag
        shadowing = Element('shadowing')                            # no - exists
        local = Element('local')                                    # no - exists
        inherited = Element('inherited', {'attribute':'value'})     # no - exists
        local_unique = Element('local', {'name':'unique'})          # ok - diff name
        path = Element('path', {'name':'2.5th path'})               # ok - diff name

        self.assert_(p.find('a/pretty/deep').get('attribute') is None)
        r = p.root_node()
        self.assert_(p.insert_node( new, r) is not None)
        self.assert_(p.insert_node( shadowing, r) is None)
        self.assert_(p.insert_node( local, r) is None)
        self.assert_(p.insert_node( inherited, r) is None)
        self.assert_(p.insert_node( local_unique, r) is not None)
        nth = p.insert_node(path, p.find('a/pretty/deep'), 1)
        self.assert_(nth is path) # inserting a node should return the inserted node

        self.assert_(p.find('local', name = 'unique') is local_unique)
        # inserting path should have made <a/pretty/deep/path> local all the way up
        self.assert_(p.find('a/pretty/deep').get('inherited') is None)
        self.assert_(p.find('a').get('inherited') is None)
        # it should also have inserted the node between the first and the second node
        self.assert_(p.find('a/pretty/deep')[1] is path)

if __name__ == '__main__':
    opus_unittest.main()
