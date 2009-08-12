"""
  UrbanSim software.
  Copyright (C) 1998-2003 University of Washington
  
  You can redistribute this program and/or modify it under the
  terms of the GNU General Public License as published by the
  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  file LICENSE.htm for copyright and licensing information, and the
  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.

"""

import os
import MySQLdb
import random

def random(N):
    """random sampling N alternatives from the universe of alternatives"""
    table_name = ''
    individual.id = ''
    alternative.table = ''
    query = 'select ' + individual.id + ',' + Geography.level1.id + ' from ' + table_name
    alternatives = 'select ' + Geography.level1.id + ' from ' + alternative.table
    for individual in individuals:
        insert_choose(individual, alternative)
        i = 0
        while i < N:
            alternatvie = random.choice(alternatives)
            if alternative == individuals[chosen]:
                next
            elif insert_non_chosen()

def stratified(N):
    
            
class Geogrpahy:
    level1.id = ''
    level2.id = ''
    level3.id = ''
    link_table = ''
    #constraint_table = ''

if __name__ = "__main__":
    mysql_hostname = ''
    mysql_username = ''
    mysql_password = ''
    mysql_database = ''
    if (os.environ.has_key('MYSQLHOSTNAME')):
        mysql_hostname = os.environ['MYSQLHOSTNAME']
    if (os.environ.has_key('MYSQLUSERNAME')):
        mysql_username = os.environ['MYSQLUSERNAME']
    if (os.environ.has_key('MYSQLPASSWORD')):
        mysql_password = os.environ['MYSQLPASSWORD']
