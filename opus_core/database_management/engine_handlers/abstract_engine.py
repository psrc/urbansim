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

class AbstractDatabaseEngineManager(object):
    
    def get_connection_string(self, database_name = None, scrub = False):
        raise Exception('method not implemented')
    
    def create_database(self, engine, database_name):
        raise Exception('method not implemented')
        
    def drop_database(self, engine, database_name):
        raise Exception('method not implemented')
    
    def has_database(self, engine, database_name):
        raise Exception('method not implemented')
    
    def create_default_database_if_absent(self, server_config):
        raise Exception('method not implemented')