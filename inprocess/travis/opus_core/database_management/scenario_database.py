#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import re

from opus_core.store.opus_database import OpusDatabase, _log_sql
from opus_core.logger import logger

'''This class supports chained databases'''
class ScenarioDatabase(OpusDatabase):
    def __init__(self, hostname=None, username=None, password=None, database_name=None, 
                 show_output=False) :
        OpusDatabase.__init__(self, 
                              hostname=hostname, 
                              username=username, 
                              password=password, 
                              database_name=database_name, 
                              show_output=show_output)
        self._table_2_db_dict = {}
        self._create_table_mapping(self.database_name)
        
    def cursor( self ) :
        return db.cursor
            
    def scenario_name( self ) :
        cursor = self.db.cursor()
        try:
            '''description is a column in a scenario_information table'''
            sql = "SELECT DESCRIPTION FROM " + self.database_and_table_for("scenario_information") + ";"
            _log_sql(sql)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows[0][0]
        except:
            return self.database_name
        
    def database_name_for(self, table_name):
        if table_name in self._table_2_db_dict.keys() :
            return self._table_2_db_dict[table_name]

    def has_table(self, table_name):
        """Returns True if this table is this scenario database's chain."""
        return self._table_2_db_dict.has_key(table_name)
    
    def get_tables_in_database(self):
        """Returns a list of the tables in this database chain."""
        return self._table_2_db_dict.keys()
        
    def get_table_mapping(self):
        """Returns dictionary mapping table names to database names.
        
        Useful for determining which database in the scenario database chain 
        contains this table."""
        return self._table_2_db_dict
        
    def _create_table_mapping(self, database_name):
        from MySQLdb import connect    
        db = connect(host=self.hostname, user=self.username, passwd=self.password, db=database_name)
        cursor = db.cursor()
        sql = "SHOW TABLES;"
        _log_sql(sql, self.show_output)
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows :
            table_name = row[0]
            if table_name not in self._table_2_db_dict.keys() :
                self._table_2_db_dict[table_name] = database_name 
                logger.log_status('Found: ' + database_name + "." + table_name,
                                   tags=['database'], verbosity_level=3)

        
        sql = "SELECT PARENT_DATABASE_URL FROM scenario_information;"
        _log_sql(sql, self.show_output)
        
        
        try:
            cursor.execute(sql)
            
        except:
            logger.log_warning("Did not find table 'scenario_information' in database '%s'; "
                               "assuming there are no more databases in this chain." % database_name)
        else:      
            try:
                rows = cursor.fetchall()
                if (not rows[0][0]) or (len(rows[0][0]) < 1) :
                    # no more parents to traverse
                    return
                match = re.search("jdbc:mysql://[^/]*/(.*)", rows[0][0])
                if match == None :
                    raise ValueError("parent database url is not a MySQL JDBC url" )
                next_database_name = match.group(1)
                
            finally:
                cursor.close()
                db.close()
        
            self._create_table_mapping(next_database_name)
            
        return
