# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from os.path import join

from opus_core.opus_exceptions.schema_exception import SchemaException
from opus_core.opus_package_info import package
from opus_core.logger import logger
from xml.dom.minidom import parse, parseString

class TableTypeSchema(dict):
    """A schema for a database table.  
    Can be used to automatically create a database table."""
    def __init__(self, table_path = ''):
        self.initiate_table_path(table_path)

    ### TODO: Generalize this to find opus packages that are not necessarily siblings to opus_core.
    def initiate_table_path(self, table_path):
        """self.table_path: contains list of directory to search for the xml schema
        Search in the directories directly in  If a .../docs/database_tables exists then add it to the path. """
        
        parent_dir_path = package().get_package_parent_path()
        
        opus_corehome = parent_dir_path
        
        dirs_in_opus_core = filter(lambda name: name.find('.') == -1, os.listdir(opus_corehome))
        self.tables_path = map(lambda dir_name: join(opus_corehome, dir_name, 'docs','database_tables'), dirs_in_opus_core)
        self.tables_path = filter(lambda path: os.path.exists(path), self.tables_path)
        if table_path:
            self.tables_path.insert(0, table_path)

    def get_path_to_table_xml_file(self, table_name, look_up_path):
        """Given a table name and a look up directory, this method will search
        for [table_name].xml, it also search paths in self.tables_path."""
        for p in [look_up_path] + self.tables_path:
            table_path = join(p, table_name.lower()+'.xml')
            #logger.log_status('searching ' + table_path)
            if os.path.exists(table_path):
#                logger.log_status('found ' + table_name + '.xml on ' + table_path)
                return table_path
        return ''
        
    def get_table_schema(self, table_name, look_up_path=''):
        """Given a table_name, and an optional look_up directory,
        This method will search [table_name].xml in look_up_path.
        If look_up_path is not given, it will search for the current directory
        of this table_type_schema.py file + default path
            Return an un-ordered dictionary at this point
        """
        if not table_name:
            return {}
        table_path = self.get_path_to_table_xml_file(table_name, look_up_path)
        if not table_path:
            raise SchemaException, 'Cannot locate xml file for table %s' % table_name
            return {}
        
        dom = parse(table_path)
        # old code using xpath:
        # col_names = xpath.Evaluate("table[name='" + table_name + "']/schema/column/@name", dom)
        # col_types = xpath.Evaluate("table[name='" + table_name + "']/schema/column/@type", dom)
        root = dom.documentElement
        # check that root has a child node with the tag 'name' and text value table_name
        # if not return the empty dictionary
        ok = False
        for c in root.childNodes:
            if c.nodeType==c.ELEMENT_NODE and c.tagName=='name' and c.firstChild.nodeValue==table_name:
                ok = True
        if not ok:
            return {}
        schemaNodes = filter(lambda n: n.nodeType==n.ELEMENT_NODE and n.tagName=='schema', root.childNodes)
        columnNodes = []
        for s in schemaNodes:
            columnNodes.extend(filter(lambda n: n.nodeType==n.ELEMENT_NODE and n.tagName=='column', s.childNodes))
        col_names = map(lambda n: str(n.getAttribute('name')).lower(), columnNodes)
        col_types = map(lambda n: str(n.getAttribute('type')), columnNodes)
        if len(col_names) == len(col_types):            
            schema = zip(col_names, col_types)
            return dict(schema)
        else:
            return {}
            
    def get_table_schema_pairlist(self, table_name, look_up_path=''):
        """return a list of pairs instead of return a dictionary"""
        schema = self.get_table_schema(table_name, look_up_path)
        schema_pairlist = []
        if not schema:
            return schema_pairlist
        for key, value in schema.iteritems():
            schema_pairlist.append((key, value))
        return schema_pairlist

from opus_core.tests import opus_unittest
import tempfile
from os.path import join
class TableTypeSchemaTests(opus_unittest.OpusTestCase):
    """Test table type schema by creating a xml file"""
    
    def setUp(self):            
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.file_name = join(self.temp_dir, 'annual_relocation_rates_for_households.xml')
        f = open(self.file_name, 'w')
        table_schema = """<?xml version="1.0" encoding="UTF-8" ?>
        <table>
            <name>annual_relocation_rates_for_households</name>
            <databases-that-contain-this-table baseyear="true" scenario="true"/>
            <fit-test>medium-tests/test_annual_relocation_rates_for_households.html</fit-test>
            <top-descriptive-text>
                The annual relocation rates for households, by combination of age and income of
                household. These values are the probabilities that a household with the given
                characteristics will relocate within the time span of one year. They do not alter from
                year to year. This table is only used by the <a href="../../models/household_relocation_choice_model.html">Household Relocation Choice Model</a>.
            </top-descriptive-text>
            <schema>  
                <column name="AGE_MIN"    type="INTEGER">The minimum age for which this probability is valid.</column>
                <column name="AGE_MAX"    type="INTEGER">The maximum age for which this probability is valid, -1 means no maximum</column>
                <column name="INCOME_MIN" type="INTEGER">The minimum income for which this probability is valid.</column>
                <column name="INCOME_MAX" type="INTEGER">The maximum income for which this probability is valid, -1 means no maximum</column>
                <column name="PROBABILITY_OF_RELOCATING" type="FLOAT">The probability of relocating in a year.</column>
            </schema>
            <end-descriptive-text>Some description...</end-descriptive-text>
        </table>
        """
        f.write(table_schema)
        f.close()
        
    def tearDown(self):            
        os.remove(self.file_name)
        
    def test_get_path_to_table_xml_file(self):
        self.assert_(TableTypeSchema().get_path_to_table_xml_file('annual_relocation_rates_for_households', self.temp_dir) != '')

    def test_get_table_schema(self):
        """this test is intended for a list of pair, not a dictionry"""
        expected_table_schema = [('AGE_MIN', 'INTEGER'), ('AGE_MAX', 'INTEGER'), ('INCOME_MIN', 'INTEGER'),
                                 ('INCOME_MAX', 'INTEGER'), ('PROBABILITY_OF_RELOCATING', 'FLOAT')]
        expected_table_schema = map(lambda (x,y): (x.lower(), y), expected_table_schema)
        table_schema = TableTypeSchema().get_table_schema_pairlist('table1', self.temp_dir)
        self.assert_(len(expected_table_schema) == len(table_schema))
        for field in expected_table_schema:
            if field not in table_schema:
                self.assert_(False, 'table schema not matched in ' + str(field))
        for field in table_schema:
            if field not in expected_table_schema:
                self.assert_(False, 'table schema not matched in ' + str(field))
        
    def test_tables_from_default_location(self):
        table_schema = TableTypeSchema().get_table_schema('table2')
        table_schema = TableTypeSchema().get_table_schema('table3')
    
if __name__ == "__main__":
    opus_unittest.main()