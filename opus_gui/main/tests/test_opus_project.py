# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.main.opus_project import *

from opus_core.tests import opus_unittest
from lxml.etree import Element
import shutil

class OpusProjectTestCase(opus_unittest.OpusTestCase):
    TESTDATA = 'testdata'
    
    def _get_data_path(self, testdata):
        testdatapath = os.path.split(__file__)[0]
        testdatapath = os.path.join(testdatapath, testdata)
        return testdatapath

    def setUp(self, testdata=TESTDATA):
        # Validate that the test data is present
        self.testdatapath = self._get_data_path(testdata)
        self.testfile_valid = os.path.join(self.testdatapath, 'project_valid.xml')
        self.testfile_invalid = os.path.join(self.testdatapath, 'project_invalid.xml')
        self.p = OpusProject()


    def _get_file_path(self, fn):
        return os.path.join(self.testdatapath, fn)

    def _open(self, fn):
        fn = self._get_file_path(fn)
        ok, msg = self.p.open(fn)
        if not ok:
            print msg
        self.assertTrue(self.p.is_open(), 'Project file could not be opened')
        return self.p

class OpusProjectModifyingTestCase(OpusProjectTestCase):
    TESTDATA_TMP = 'testdata.tmp'

    def setUp(self):
        testdatapath = self._get_data_path(self.TESTDATA)
        testdatapath_tmp = self._get_data_path(self.TESTDATA_TMP)
        if os.path.exists(testdatapath_tmp):
            shutil.rmtree(testdatapath_tmp, False)
        shutil.copytree(testdatapath, testdatapath_tmp)
        OpusProjectTestCase.setUp(self, testdatapath_tmp)

    def tearDown(self):
        shutil.rmtree(self.testdatapath, False)
        OpusProjectTestCase.tearDown(self)

class TestOpusProject(OpusProjectTestCase):
    ''' Test suite for Opus Project '''

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
        def get_nodes_by_name_as_list(names):
            return [p.find(name) for name in names]
            
        p = self._open('child.xml')
        i_names = ('inherited', 'a/pretty/deep/inherited')
        s_names = ('shadowing', 'a/pretty/deep/shadowing')
        l_names = ('local', 'a/pretty/deep/local', 'another/pretty/deep/local')
        il_start = get_nodes_by_name_as_list(i_names)
        sl_start = get_nodes_by_name_as_list(s_names)
        ll_start = get_nodes_by_name_as_list(l_names)
        
        # shadowing node should be only the following nodes:
        # - three nodes: opus_project, general and shadowing
        # - four nodes: a, pretty, deep, shadowing
        for s in sl_start:
            self.assertTrue(s in p._shadowing_nodes)
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        self.assertEqual(len(p._shadowing_nodes), 7)

        # delete nodes and assert that nothing changes the inherited tree (orignal values for nodes)
        inherited_tree_start = tostring(p._inherited_root)
        
        for start in il_start + ll_start:
            ins = p.delete_node(start)
            self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
            # test that only removing shadowing nodes returns inserted nodes
            self.assertTrue(ins is None)
        for start in sl_start:
            ins = p.delete_node(start)
            self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
            # test that only removing shadowing nodes returns inserted nodes
            self.assertTrue(ins is not None)

        il_end = get_nodes_by_name_as_list(i_names)
        sl_end = get_nodes_by_name_as_list(s_names)
        ll_end = get_nodes_by_name_as_list(l_names)

        for start, end in zip(il_start, il_end):
            self.assertTrue(start is end) # delete inherited should leave the node intact
        for end in sl_end:
            self.assertTrue(end.get('inherited') is not None)
            self.assertEqual(end.text, 'parent_value', 'delete shadowing node reinserts inherited')
        for end in ll_end:
            self.assertTrue(end is None) # deleting locals removes them

        # check that the shadowing node was removed from the shadowing nodes map
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        # run multiple passes of making local and deleting inherited nodes -- some things vary
        # when doing this (like which nodes that are readded), so it's useful to test it
        for name in i_names:
            for nth in range(1, 3):
                i = p.find(name)
                p.make_local(i)
                i_ins = p.delete_node(i)
                i = p.find(name)
                s = 'pass #%d of make_local/delete_node failed for node %s' % (nth, node_identity_string(i))
                self.assert_(i_ins is i, s)
                self.assert_(i not in p._shadowing_nodes, s)
                self.assert_(i is not None, s)
                self.assert_(i.get('inherited') is not None, s)

    def test_update_node(self):
        def get_nodes_by_name_as_list(names):
            return [p.find(name) for name in names]
            
        p = self._open('child.xml')
        i_names = ('inherited', 'a/pretty/deep/inherited')
        s_names = ('shadowing', 'a/pretty/deep/shadowing')
        l_names = ('local', 'a/pretty/deep/local', 'another/pretty/deep/local')
        il_start = get_nodes_by_name_as_list(i_names)
        sl_start = get_nodes_by_name_as_list(s_names)
        ll_start = get_nodes_by_name_as_list(l_names)
        
        # shadowing node should be only the following nodes:
        # - three nodes: opus_project, general and shadowing
        # - four nodes: a, pretty, deep, shadowing
        for s in sl_start:
            self.assertTrue(s in p._shadowing_nodes)
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        self.assertEqual(len(p._shadowing_nodes), 7)

        # updated nodes and assert that nothing changes the inherited tree (orignal values for nodes)
        inherited_tree_start = tostring(p._inherited_root)
        
        for start in il_start:
            start_copy = copy.deepcopy(start)
            start_copy.text += ' appended_text'
            ins = p.delete_or_update_node(start, start_copy)
            self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
            self.assertTrue(ins is None)
            
        for start in ll_start + sl_start:
            start_copy = copy.deepcopy(start)
            start_copy.text += ' appended_text'
            ins = p.delete_or_update_node(start, start_copy)
            self.assertEqual(inherited_tree_start, tostring(p._inherited_root))
            self.assertTrue(ins is not None)

        il_end = get_nodes_by_name_as_list(i_names)
        sl_end = get_nodes_by_name_as_list(s_names)
        ll_end = get_nodes_by_name_as_list(l_names)
        
        for start, end in zip(il_start, il_end):
            self.assertTrue(start is end) # update inherited is a no-op and should leave the node intact
        for end in sl_end:
            self.assertTrue(end.get('inherited') is None)
            self.assertEqual(end.text, 'shadowed_value_child appended_text', 'update shadowing node changes text')
        for end in ll_end:
            self.assertTrue(end.get('inherited') is None)
            print end.text
            self.assertEquals(end.text, 'local appended_text', 'update shadowing node changes text')

        # check that the shadowing node was removed from the shadowing nodes map
        self.assertTrue(p.root_node() in p._shadowing_nodes)
        self.assertTrue(p.find('general') in p._shadowing_nodes)
        # run multiple passes of making local and deleting inherited nodes -- some things vary
        # when doing this (like which nodes that are readded), so it's useful to test it
        for name in i_names:
            for nth in range(1, 3):
                i = p.find(name)
                p.make_local(i)
                ic = p.delete_or_update_node(i, copy.deepcopy(i))
                i_ins = p.delete_node(ic)
                i = p.find(name)
                s = 'pass #%d of make_local/delete_node failed for node %s' % (nth, node_identity_string(i))
                self.assert_(i_ins is i, s)
                self.assert_(i not in p._shadowing_nodes, s)
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
        
        
    # ============================================
    # Tests for collecting templated project nodes
    # ============================================
    
    def test_get_template_nodes_with_model_template_filter(self):
        p = self._open('templated_project_nodes_with_model_templates.xml')
        
        expected_keys_with_out_model_templates = ['template_from_child', 'template_from_parent']
        expected_keys_with_out_model_templates.sort()
        
        expected_keys_with_model_templates = expected_keys_with_out_model_templates + \
            ['model_template_child', 'model_template_parent']
        expected_keys_with_model_templates.sort()

        # Fetch with out model templates nodes
        collected_keys = [node.get('field_identifier') for node in p.get_template_nodes()]
        collected_keys.sort()
        
        self.assertEqual(collected_keys, expected_keys_with_out_model_templates)
        
        # fetch with model templates
        collected_keys = [node.get('field_identifier') for node in p.get_template_nodes(skip_model_templates = False)]
        collected_keys.sort()
        
        self.assertEqual(collected_keys, expected_keys_with_model_templates)
        
        # validate that the default is to fetch templates without the model templates
        collected_keys = [node.get('field_identifier') for node in p.get_template_nodes(skip_model_templates = True)]
        collected_keys_default = [node.get('field_identifier') for node in p.get_template_nodes()]
        self.assertEqual(collected_keys, collected_keys_default)


    def test_get_template_nodes_single_level(self):
        p = self._open('templated_project_nodes_single_level.xml')
        
        expected_keys = ['template_one', 'template_two']
        expected_keys.sort()
        
        collected_template_keys = [node.get('field_identifier') for node in p.get_template_nodes()]
        collected_template_keys.sort()
        
        self.assertEqual(collected_template_keys, expected_keys)
        
        
    def test_get_template_nodes_multi_level(self):
        p = self._open('templated_project_nodes_multi_level.xml')
        
        expected_keys = ['template_from_base', 
                         'template_from_parent', 
                         'parent', # this field_identifier is overwriting the same node "grandparent" in the grandparent
                         'template_from_grandparent']
        expected_keys.sort()

        collected_template_keys = [node.get('field_identifier') for node in p.get_template_nodes()]
        collected_template_keys.sort()
        
        self.assertEqual(collected_template_keys, expected_keys)


class TestOpusProjectWithSave(OpusProjectModifyingTestCase):
    def test_copy_to_parent(self):
        p = self._open('templated_project_nodes_multi_level.xml')

        id_strings = (
                      '/results_manager:/copy_this_to_parent:',
                      '/results_manager:/add_this_to_parent:/copy_this_to_parent:',
                      '/results_manager:/deep_copy_this_to_parent:',
                      '/results_manager:/merge_this_with_parent:/copy_this_to_parent:',
                      '/results_manager:/overwrite_this_in_parent:/already_in_parent:',
                      '/results_manager:/grandparent_based_children:',
                      )
        for id_string in id_strings:
            n = p.find_by_id_string(id_string)
            p.copy_to_parent(n)
        
        self.assertEqual(file(self._get_file_path('templated_project_nodes_multi_level_parent.xml')).read(),
                         file(self._get_file_path('templated_project_nodes_multi_level_parent_after_copy.xml')).read(),
                         'Merge works as expected')

if __name__ == '__main__':
    opus_unittest.main()
