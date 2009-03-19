# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from numpy import where, arange
from opus_core.logger import logger

class ModelGroup(object):
    """Used for creating a model group with several members."""
    def __init__(self, dataset, grouping_attribute):
        """'dataset' is a Dataset representing the grouping table.
           'grouping_attribute' is the name of dataset's attribute that determines the names of the group members.
           Values of the id attribute of dataset are the numeric codes of the group members.
        """
        self.dataset = dataset
        self.grouping_attribute = grouping_attribute
        self.grouping_codes = dataset.get_id_attribute()
        self.grouping_names = dataset.get_attribute(grouping_attribute)

    def get_member_name(self, code):
        idx = self.get_member_index_by_code(code)
        return self.grouping_names[idx]

    def get_member_index_by_name(self, name):
        return where(self.grouping_names == name)[0]

    def get_member_index_by_code(self, code):
        return where(self.grouping_codes == code)[0]

    def get_member_code_by_index(self, index):
        return self.grouping_codes[index]

    def get_member_names(self):
        return self.grouping_names

    def get_attributes_of_grouping_dataset(self):
        return dataset.get_known_attribute_names()

    def get_grouping_attribute(self):
        return self.grouping_attribute

class ModelGroupMember(object):
    def __init__(self, model_group, member_name):
        self.model_group = model_group
        self.member_name = member_name
        self.member_index = None
        if isinstance(model_group, ModelGroup):
            self.member_index = model_group.get_member_index_by_name(member_name)
        self.member_code = None
        if self.member_index is not None:
            self.member_code = model_group.get_member_code_by_index(self.member_index)
        self.agents_grouping_attribute = None

    def get_member_name(self):
        return self.member_name

    def get_member_index(self):
        return self.member_index

    def get_member_code(self):
        return self.member_code

    def get_attribute_value(self, attribute):
        return self.model_group.dataset.get_attribute_by_index(attribute, self.get_member_index())

    def get_values_of_all_attributes(self):
        result = {}
        for attr in self.model_group.get_attributes_of_grouping_dataset():
            result[attr] = self.get_attribute_value(attr)
        return result

    def set_agents_grouping_attribute(self, attribute):
        self.agents_grouping_attribute = attribute
        logger.log_status("'agents_grouping_attribute' set to %s." % self.agents_grouping_attribute)

    def get_agents_grouping_attribute(self):
        return self.agents_grouping_attribute

    def get_index_of_my_agents(self, dataset, index, dataset_pool=None, resources=None):
        agents_grouping_attr = self.get_agents_grouping_attribute()
        if agents_grouping_attr is None:
            logger.log_warning("'agents_grouping_attribute' wasn't set. No agent selection was done.")
            logger.log_note("Use method 'set_agents_grouping_attribute' for agents selection.")
            return arange(index.size)
        dataset.compute_variables(agents_grouping_attr, dataset_pool=dataset_pool, resources=resources)
        code_values = dataset.get_attribute_by_index(agents_grouping_attr, index)
        return where(code_values == self.get_member_code())[0]

    def add_member_prefix_to_table_names(self, tables):
        """
        Takes a list of strings--table names--and returns a list of the table
        names with the ModelGroup's member name prepended. If any of the table
        names in the list are None, the corresponding entry in the resulting
        list will also be None.
        """
        result = []
        for table in tables:
            result.append(self.add_member_prefix_to_table_name(table))
        return result

    def add_member_prefix_to_table_name(self, table):
        """
        Takes a string--table name--and returns the table
        name with the ModelGroup's member name prepended
        """
        if (table is not None):
            result = "%s_%s" % (self.get_member_name(), table)
        else:
            result = None
        return result


from opus_core.tests import opus_unittest


class TestModelGroupMember(opus_unittest.TestCase):
    def setUp(self):
        self.model_group_member = ModelGroupMember(None, 'model_name')

    def tearDown(self):
        pass

    def test_add_member_prefix_to_table_names(self):
        expected_table_names = ['model_name_table_name1', 'model_name_table_name2']

        actual_table_names = self.model_group_member.add_member_prefix_to_table_names(['table_name1', 'table_name2'])

        self.assertEqual(actual_table_names, expected_table_names,
            msg = 'Table names returned by add_member_prefix_to_table_names different than expected. Expected %s. Received %s.'
                % (expected_table_names, actual_table_names))

        expected_table_names = ['model_name_table_name3', None, 'model_name_table_name5']

        actual_table_names = self.model_group_member.add_member_prefix_to_table_names(['table_name3', None, 'table_name5'])

        self.assertEqual(actual_table_names, expected_table_names,
            msg = 'Table names returned by add_member_prefix_to_table_names different than expected. Expected %s. Received %s.'
                % (expected_table_names, actual_table_names))

        try:
            self.model_group_member.add_member_prefix_to_table_names(None)
        except:
            pass
        else:
            self.fail('Expected failure of add_member_prefix_to_table_names '
                'with None for the tables parameter, but it did not fail.')

    def test_add_member_prefix_to_table_name(self):
        expected_table_name = 'model_name_table_name'
        actual_table_name = self.model_group_member.add_member_prefix_to_table_name('table_name')
        self.assertEqual(expected_table_name, actual_table_name,
            msg = 'Table name returned by add_member_prefix_to_table_name different than expected. Expected %s. Received %s.'
                % (expected_table_name, actual_table_name))
        self.assertEqual(None, self.model_group_member.add_member_prefix_to_table_name(None), 'None expected as result')


if __name__ == '__main__':
    opus_unittest.main()